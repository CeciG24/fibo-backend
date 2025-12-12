from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Ejemplo de ruta
@auth_bp.route("/login")
def login():
    return {"msg": "login ok"}
