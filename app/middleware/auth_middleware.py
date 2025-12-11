"""
Custom middleware decorators for authentication and authorization.
"""
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User
from app.models import db
from datetime import datetime, timedelta
import os


def admin_required(fn):
    """
    Decorator que requiere que el usuario sea admin (plan enterprise).
    
    Usage:
        @bp.route('/admin/users')
        @jwt_required()
        @admin_required
        def list_all_users():
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        if user.plan != 'enterprise':
            return jsonify({
                "error": "Acceso denegado",
                "message": "Esta funcionalidad requiere plan Enterprise"
            }), 403
        
        return fn(*args, **kwargs)
    
    return wrapper


def verified_required(fn):
    """
    Decorator que requiere que el usuario tenga email verificado.
    
    Usage:
        @bp.route('/premium-feature')
        @jwt_required()
        @verified_required
        def premium_feature():
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        if not user.is_verified:
            return jsonify({
                "error": "Email no verificado",
                "message": "Por favor verifica tu email para acceder a esta funcionalidad"
            }), 403
        
        return fn(*args, **kwargs)
    
    return wrapper


def check_generation_limit(fn):
    """
    Decorator que verifica si el usuario puede generar más imágenes.
    
    Usage:
        @bp.route('/generate')
        @jwt_required()
        @check_generation_limit
        def generate_image():
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        if not user.can_generate():
            return jsonify({
                "error": "Límite de generaciones alcanzado",
                "message": f"Has alcanzado tu límite diario de generaciones",
                "plan": user.plan,
                "upgrade_url": "/pricing"
            }), 429
        
        return fn(*args, **kwargs)
    
    return wrapper


def plan_required(required_plan='pro'):
    """
    Decorator que requiere un plan mínimo específico.
    
    Args:
        required_plan: 'free', 'pro', o 'enterprise'
    
    Usage:
        @bp.route('/pro-feature')
        @jwt_required()
        @plan_required('pro')
        def pro_feature():
            ...
    """
    plan_hierarchy = {
        'free': 0,
        'pro': 1,
        'enterprise': 2
    }
    
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({"error": "Usuario no encontrado"}), 404
            
            user_plan_level = plan_hierarchy.get(user.plan, 0)
            required_plan_level = plan_hierarchy.get(required_plan, 0)
            
            if user_plan_level < required_plan_level:
                return jsonify({
                    "error": "Plan insuficiente",
                    "message": f"Esta funcionalidad requiere plan {required_plan.title()}",
                    "current_plan": user.plan,
                    "upgrade_url": "/pricing"
                }), 403
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def log_request(fn):
    """
    Decorator que registra información de la request (para debugging).
    
    Usage:
        @bp.route('/debug-endpoint')
        @log_request
        def debug_endpoint():
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"[{datetime.utcnow()}] {request.method} {request.path}")
        print(f"  Headers: {dict(request.headers)}")
        print(f"  Args: {request.args}")
        if request.is_json:
            print(f"  JSON: {request.get_json()}")
        
        response = fn(*args, **kwargs)
        
        print(f"  Response: {response}")
        return response
    
    return wrapper


def owner_required(resource_model, id_param='id'):
    """
    Decorator que verifica que el usuario sea dueño del recurso.
    
    Args:
        resource_model: Modelo a verificar (Project, Generation, etc.)
        id_param: Nombre del parámetro en la URL
    
    Usage:
        @bp.route('/projects/<int:project_id>')
        @jwt_required()
        @owner_required(Project, 'project_id')
        def get_project(project_id):
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            
            # Obtener el ID del recurso desde kwargs
            resource_id = kwargs.get(id_param)
            if not resource_id:
                return jsonify({"error": "ID de recurso no proporcionado"}), 400
            
            # Buscar el recurso
            resource = resource_model.query.get(resource_id)
            if not resource:
                return jsonify({"error": "Recurso no encontrado"}), 404
            
            # Verificar ownership
            if resource.user_id != current_user_id:
                return jsonify({
                    "error": "Acceso denegado",
                    "message": "No tienes permiso para acceder a este recurso"
                }), 403
            
            # Pasar el recurso a la función (opcional, útil para evitar otra query)
            kwargs['resource'] = resource
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator
