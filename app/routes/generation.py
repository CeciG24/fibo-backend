from flask import Blueprint, request, jsonify, send_file
from app.services.fibo_service import FIBOService
from app.models.scene import Scene
from app.models.camera import CameraSettings
from app.models.lighting import LightingSetup
import os

bp = Blueprint('generation', __name__)
fibo_service = FIBOService()

@bp.route('/single', methods=['POST'])
def generate_single_frame():
    """Genera un solo frame con los parámetros dados"""
    try:
        data = request.get_json()
        
        # Construir la escena
        camera = CameraSettings(
            angle=data.get('camera', {}).get('angle', 'eye_level'),
            shot_type=data.get('camera', {}).get('shot_type', 'medium_shot'),
            fov=data.get('camera', {}).get('fov', 50.0),
            focal_length=data.get('camera', {}).get('focal_length', 50.0),
            aperture=data.get('camera', {}).get('aperture', 2.8)
        )
        
        lighting = LightingSetup(
            preset=data.get('lighting', {}).get('preset', 'three_point'),
            time_of_day=data.get('lighting', {}).get('time_of_day', 'golden_hour'),
            color_grading=data.get('lighting', {}).get('color_grading', 'neutral')
        )
        
        scene = Scene(
            prompt=data['prompt'],
            negative_prompt=data.get('negative_prompt', ''),
            camera=camera,
            lighting=lighting,
            width=data.get('width', 1024),
            height=data.get('height', 576),
            seed=data.get('seed')
        )
        
        # Generar con FIBO
        payload = scene.to_fibo_payload()
        result = fibo_service.generate_image(payload)
        
        if 'error' in result:
            return jsonify({"error": result['error']}), 500
            
        return jsonify({
            "success": True,
            "image_url": result.get('image_url'),
            "generation_id": result.get('id'),
            "parameters": payload
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/sequence', methods=['POST'])
def generate_sequence():
    """Genera una secuencia de frames (storyboard)"""
    try:
        data = request.get_json()
        scenes_data = data.get('scenes', [])
        
        scenes = []
        for scene_data in scenes_data:
            # Similar al single frame pero para múltiples escenas
            scene = Scene(
                prompt=scene_data['prompt'],
                camera=CameraSettings(**scene_data.get('camera', {})),
                lighting=LightingSetup(**scene_data.get('lighting', {}))
            )
            scenes.append(scene.to_fibo_payload())
        
        results = fibo_service.generate_sequence(scenes)
        
        return jsonify({
            "success": True,
            "frames": results,
            "total": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/status/<generation_id>', methods=['GET'])
def get_status(generation_id):
    """Obtiene el estado de una generación"""
    result = fibo_service.get_generation_status(generation_id)
    return jsonify(result)