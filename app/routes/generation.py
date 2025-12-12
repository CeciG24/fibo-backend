from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.services.fibo_service import FIBOService
from app.models.scene import Scene
from app.models.camera import CameraSettings
from app.models.lighting import LightingSetup
from app.models.user import User
from app.models.project import Generation
from app.models import db
import time

generation_bp = Blueprint('generation', __name__, url_prefix='/generation')
fibo_service = FIBOService()

@generation_bp.route('/health', methods=['GET'])
def health_check():
    """Verifica el estado de la conexión con FIBO"""
    health = fibo_service.health_check()
    return jsonify(health), 200

@generation_bp.route('/single', methods=['POST'])
@jwt_required()
def generate_single_frame():
    """Genera un solo frame con los parámetros dados"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # Verificar límite de generaciones
        if not user.can_generate():
            return jsonify({
                "error": "Has alcanzado tu límite diario de generaciones",
                "remaining": 0,
                "upgrade_url": "/pricing"
            }), 429
        
        data = request.get_json()
        
        if not data or not data.get('prompt'):
            return jsonify({"error": "El prompt es requerido"}), 400
        
        # Crear registro de generación
        generation = Generation(
            user_id=user.id,
            project_id=data.get('project_id'),
            prompt=data['prompt'],
            negative_prompt=data.get('negative_prompt', ''),
            status='generating'
        )
        
        db.session.add(generation)
        db.session.commit()
        
        try:
            # Construir la escena
            camera = CameraSettings(
                angle=data.get('camera', {}).get('angle', 'eye_level'),
                shot_type=data.get('camera', {}).get('shot_type', 'medium_shot'),
                fov=data.get('camera', {}).get('fov', 50.0),
                focal_length=data.get('camera', {}).get('focal_length', 50.0),
                aperture=data.get('camera', {}).get('aperture', 2.8),
                composition_rule=data.get('camera', {}).get('composition_rule', 'rule_of_thirds'),
                depth_of_field=data.get('camera', {}).get('depth_of_field', 'medium')
            )
            
            lighting = LightingSetup(
                preset=data.get('lighting', {}).get('preset', 'three_point'),
                time_of_day=data.get('lighting', {}).get('time_of_day', 'golden_hour'),
                color_grading=data.get('lighting', {}).get('color_grading', 'neutral'),
                ambient_intensity=data.get('lighting', {}).get('ambient_intensity', 0.3)
            )
            
            scene = Scene(
                prompt=data['prompt'],
                negative_prompt=data.get('negative_prompt', ''),
                camera=camera,
                lighting=lighting,
                width=data.get('width', 1024),
                height=data.get('height', 576),
                steps=data.get('steps', 30),
                guidance_scale=data.get('guidance_scale', 7.5),
                seed=data.get('seed'),
                style=data.get('style', 'cinematic'),
                color_palette=data.get('color_palette')
            )
            
            # Validar escena
            valid, error_msg = scene.validate()
            if not valid:
                generation.status = 'failed'
                generation.error_message = error_msg
                db.session.commit()
                return jsonify({"error": error_msg}), 400
            
            # Guardar parámetros
            generation.set_parameters(scene.to_fibo_payload())
            if scene.seed:
                generation.seed = scene.seed
            
            # Generar con FIBO
            start_time = time.time()
            payload = scene.to_fibo_payload()
            result = fibo_service.generate_image(payload)
            generation_time = time.time() - start_time
            
            # Verificar si hubo error
            if 'error' in result:
                generation.status = 'failed'
                generation.error_message = result['error']
                generation.generation_time = generation_time
                db.session.commit()
                
                return jsonify({
                    "success": False,
                    "error": result['error'],
                    "suggestion": result.get('suggestion', 'Verifica tu configuración de FIBO API'),
                    "generation_id": generation.id
                }), 500
            
            # Actualizar generación con resultado exitoso
            generation.status = 'completed'
            generation.image_url = result.get('image_url')
            generation.fibo_generation_id = result.get('id')
            generation.generation_time = generation_time
            generation.completed_at = datetime.utcnow()
            
            # Incrementar contador del usuario
            user.increment_generation_count()
            
            db.session.commit()
            
            return jsonify({
                "success": True,
                "generation": generation.to_dict(),
                "remaining_today": user.get_remaining_generations(),
                "mock_mode": result.get('mock', False)
            }), 200
            
        except Exception as e:
            generation.status = 'failed'
            generation.error_message = str(e)
            db.session.commit()
            raise e
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@generation_bp.route('/sequence', methods=['POST'])
@jwt_required()
def generate_sequence():
    """Genera una secuencia de frames (storyboard)"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        data = request.get_json()
        scenes_data = data.get('scenes', [])
        
        if not scenes_data:
            return jsonify({"error": "Se requiere al menos una escena"}), 400
        
        # Verificar límite
        remaining = user.get_remaining_generations()
        if isinstance(remaining, int) and len(scenes_data) > remaining:
            return jsonify({
                "error": f"Excedes tu límite diario. Puedes generar {remaining} más hoy",
                "remaining": remaining
            }), 429
        
        project_id = data.get('project_id')
        results = []
        
        for i, scene_data in enumerate(scenes_data):
            # Crear generación para cada escena
            generation = Generation(
                user_id=user.id,
                project_id=project_id,
                prompt=scene_data['prompt'],
                negative_prompt=scene_data.get('negative_prompt', ''),
                scene_number=i + 1,
                status='generating'
            )
            db.session.add(generation)
            db.session.commit()
            
            try:
                # Construir escena
                scene = Scene(
                    prompt=scene_data['prompt'],
                    camera=CameraSettings(**scene_data.get('camera', {})),
                    lighting=LightingSetup(**scene_data.get('lighting', {})),
                    scene_number=i + 1
                )
                
                generation.set_parameters(scene.to_fibo_payload())
                
                # Generar
                start_time = time.time()
                result = fibo_service.generate_image(scene.to_fibo_payload())
                generation_time = time.time() - start_time
                
                if 'error' in result:
                    generation.status = 'failed'
                    generation.error_message = result['error']
                else:
                    generation.status = 'completed'
                    generation.image_url = result.get('image_url')
                    generation.generation_time = generation_time
                    generation.completed_at = datetime.utcnow()
                    user.increment_generation_count()
                
                db.session.commit()
                results.append(generation.to_dict())
                
            except Exception as e:
                generation.status = 'failed'
                generation.error_message = str(e)
                db.session.commit()
                results.append(generation.to_dict())
        
        return jsonify({
            "success": True,
            "frames": results,
            "total": len(results),
            "completed": len([r for r in results if r['status'] == 'completed']),
            "failed": len([r for r in results if r['status'] == 'failed'])
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@generation_bp.route('/history', methods=['GET'])
@jwt_required()
def get_generation_history():
    """Obtiene el historial de generaciones del usuario"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        project_id = request.args.get('project_id', type=int)
        status = request.args.get('status')
        
        query = Generation.query.filter_by(user_id=current_user_id)
        
        if project_id:
            query = query.filter_by(project_id=project_id)
        
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(Generation.created_at.desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "success": True,
            "generations": [g.to_dict() for g in pagination.items],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@generation_bp.route('/<int:generation_id>', methods=['GET'])
@jwt_required()
def get_generation(generation_id):
    """Obtiene una generación específica"""
    try:
        current_user_id = get_jwt_identity()
        generation = Generation.query.filter_by(
            id=generation_id,
            user_id=current_user_id
        ).first()
        
        if not generation:
            return jsonify({"error": "Generación no encontrada"}), 404
        
        return jsonify({
            "success": True,
            "generation": generation.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@generation_bp.route('/<int:generation_id>/favorite', methods=['POST'])
@jwt_required()
def toggle_favorite(generation_id):
    """Marca/desmarca una generación como favorita"""
    try:
        current_user_id = get_jwt_identity()
        generation = Generation.query.filter_by(
            id=generation_id,
            user_id=current_user_id
        ).first()
        
        if not generation:
            return jsonify({"error": "Generación no encontrada"}), 404
        
        generation.is_favorite = not generation.is_favorite
        db.session.commit()
        
        return jsonify({
            "success": True,
            "is_favorite": generation.is_favorite
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@generation_bp.route('/<int:generation_id>', methods=['DELETE'])
@jwt_required()
def delete_generation(generation_id):
    """Elimina una generación"""
    try:
        current_user_id = get_jwt_identity()
        generation = Generation.query.filter_by(
            id=generation_id,
            user_id=current_user_id
        ).first()
        
        if not generation:
            return jsonify({"error": "Generación no encontrada"}), 404
        
        db.session.delete(generation)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Generación eliminada"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400