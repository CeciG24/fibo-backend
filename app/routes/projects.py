from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.models.project import Project
from app.models.user import User
from app.middleware import owner_required

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

# ==================== LIST ALL (del usuario actual) ====================
@projects_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    """
    Lista todos los proyectos del usuario actual.
    Query params: ?page=1&per_page=10&status=draft
    """
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        # Query base: solo proyectos del usuario
        query = Project.query.filter_by(user_id=current_user_id)
        
        # Filtro opcional por status
        if status:
            query = query.filter_by(status=status)
        
        # Ordenar por más reciente
        query = query.order_by(Project.updated_at.desc())
        
        # Paginación
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "success": True,
            "projects": [p.to_dict() for p in pagination.items],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ==================== GET ONE (verificando ownership) ====================
@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
@owner_required(Project, 'project_id')
def get_project(project_id, resource=None):
    """
    Obtiene un proyecto específico con todas sus generaciones.
    Solo el dueño puede verlo (o si es público).
    """
    try:
        # 'resource' ya viene cargado del decorator owner_required
        return jsonify({
            "success": True,
            "project": resource.to_dict(include_generations=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ==================== CREATE ====================
@projects_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    """
    Crea un nuevo proyecto.
    Body: {"title": "...", "description": "...", "aspect_ratio": "16:9"}
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validación básica
        if not data or not data.get('title'):
            return jsonify({
                "success": False,
                "error": "El título es requerido"
            }), 400
        
        # Validar que el usuario existe
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "Usuario no encontrado"
            }), 404
        
        # Crear proyecto
        project = Project(
            user_id=current_user_id,
            title=data['title'],
            description=data.get('description', ''),
            aspect_ratio=data.get('aspect_ratio', '16:9'),
            resolution=data.get('resolution', '1024x576'),
            is_public=data.get('is_public', False)
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Proyecto creado exitosamente",
            "project": project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ==================== UPDATE (solo el dueño) ====================
@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
@owner_required(Project, 'project_id')
def update_project(project_id, resource=None):
    """
    Actualiza un proyecto existente.
    Solo el dueño puede actualizarlo.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No hay datos para actualizar"
            }), 400
        
        # Actualizar solo campos permitidos
        allowed_fields = [
            'title', 'description', 'thumbnail_url', 
            'aspect_ratio', 'resolution', 'is_public', 'status'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(resource, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Proyecto actualizado exitosamente",
            "project": resource.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ==================== DELETE (solo el dueño) ====================
@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
@owner_required(Project, 'project_id')
def delete_project(project_id, resource=None):
    """
    Elimina un proyecto y todas sus generaciones.
    Solo el dueño puede eliminarlo.
    """
    try:
        db.session.delete(resource)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Proyecto eliminado exitosamente"
        }), 200  # Uso 200 en vez de 204 para poder enviar mensaje
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ==================== PROYECTOS PÚBLICOS (sin auth) ====================
@projects_bp.route('/public', methods=['GET'])
def get_public_projects():
    """
    Lista proyectos públicos (galería).
    No requiere autenticación.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        
        query = Project.query.filter_by(
            is_public=True, 
            status='completed'
        ).order_by(Project.updated_at.desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "success": True,
            "projects": [p.to_dict() for p in pagination.items],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ==================== ESTADÍSTICAS DEL PROYECTO ====================
@projects_bp.route('/<int:project_id>/stats', methods=['GET'])
@jwt_required()
@owner_required(Project, 'project_id')
def get_project_stats(project_id, resource=None):
    """
    Obtiene estadísticas del proyecto.
    """
    try:
        stats = {
            "total_generations": resource.generations.count(),
            "completed_generations": resource.generations.filter_by(status='completed').count(),
            "failed_generations": resource.generations.filter_by(status='failed').count(),
            "favorite_count": resource.generations.filter_by(is_favorite=True).count(),
            "created_at": resource.created_at.isoformat(),
            "last_updated": resource.updated_at.isoformat()
        }
        
        return jsonify({
            "success": True,
            "stats": stats
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ==================== DUPLICAR PROYECTO ====================
@projects_bp.route('/<int:project_id>/duplicate', methods=['POST'])
@jwt_required()
@owner_required(Project, 'project_id')
def duplicate_project(project_id, resource=None):
    """
    Duplica un proyecto existente.
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Crear nuevo proyecto con los mismos datos
        new_project = Project(
            user_id=current_user_id,
            title=f"{resource.title} (Copia)",
            description=resource.description,
            aspect_ratio=resource.aspect_ratio,
            resolution=resource.resolution,
            is_public=False,  # Las copias siempre privadas
            status='draft'
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Proyecto duplicado exitosamente",
            "project": new_project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
