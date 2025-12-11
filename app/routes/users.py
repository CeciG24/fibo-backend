from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.project import Project

bp = Blueprint('users', __name__)

@bp.route('/<username>', methods=['GET'])
def get_user_profile(username):
    """Obtiene el perfil público de un usuario"""
    try:
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # Solo mostrar información pública
        profile = user.to_dict(include_email=False)
        
        # Agregar estadísticas públicas
        public_projects = Project.query.filter_by(
            user_id=user.id,
            is_public=True
        ).count()
        
        profile['public_projects'] = public_projects
        
        return jsonify(profile), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/<username>/projects', methods=['GET'])
def get_user_public_projects(username):
    """Obtiene los proyectos públicos de un usuario"""
    try:
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        
        query = Project.query.filter_by(
            user_id=user.id,
            is_public=True,
            status='completed'
        ).order_by(Project.updated_at.desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "projects": [p.to_dict() for p in pagination.items],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages,
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/search', methods=['GET'])
def search_users():
    """Busca usuarios por username"""
    try:
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if not query:
            return jsonify({"error": "Query de búsqueda requerido"}), 400
        
        users_query = User.query.filter(
            User.username.ilike(f'%{query}%')
        ).filter_by(is_active=True)
        
        pagination = users_query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "users": [u.to_dict() for u in pagination.items],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400