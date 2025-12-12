from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from app.models import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registro de nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Username, email y password son requeridos"}), 400
        
        # Validar email
        try:
            email_info = validate_email(data['email'], check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            return jsonify({"error": f"Email inválido: {str(e)}"}), 400
        
        # Validar longitud de contraseña
        if len(data['password']) < 8:
            return jsonify({"error": "La contraseña debe tener al menos 8 caracteres"}), 400
        
        # Validar longitud de username
        if len(data['username']) < 3:
            return jsonify({"error": "El username debe tener al menos 3 caracteres"}), 400
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "El username ya está en uso"}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "El email ya está registrado"}), 400
        
        # Crear nuevo usuario
        user = User(
            username=data['username'],
            email=email,
            full_name=data.get('full_name', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Crear tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user": user.to_dict(include_email=True),
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login de usuario"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email y password son requeridos"}), 400
        
        # Buscar usuario
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        if not user.is_active:
            return jsonify({"error": "Cuenta desactivada"}), 403
        
        # Actualizar último login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Crear tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            "message": "Login exitoso",
            "user": user.to_dict(include_email=True),
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresca el access token usando el refresh token"""
    try:
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            "access_token": access_token
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Obtiene información del usuario actual"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        return jsonify({
            "user": user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    """Actualiza el perfil del usuario"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        data = request.get_json()
        
        # Campos actualizables
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'bio' in data:
            user.bio = data['bio']
        if 'avatar_url' in data:
            user.avatar_url = data['avatar_url']
        
        db.session.commit()
        
        return jsonify({
            "message": "Perfil actualizado exitosamente",
            "user": user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Cambia la contraseña del usuario"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        data = request.get_json()
        
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({"error": "Se requieren ambas contraseñas"}), 400
        
        # Verificar contraseña actual
        if not user.check_password(data['current_password']):
            return jsonify({"error": "Contraseña actual incorrecta"}), 401
        
        # Validar nueva contraseña
        if len(data['new_password']) < 8:
            return jsonify({"error": "La nueva contraseña debe tener al menos 8 caracteres"}), 400
        
        # Actualizar contraseña
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({
            "message": "Contraseña actualizada exitosamente"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout del usuario (invalidar token en el cliente)"""
    # En una implementación completa, aquí podrías agregar el token a una blacklist
    return jsonify({
        "message": "Logout exitoso"
    }), 200
