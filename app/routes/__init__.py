from flask import Blueprint

# Initialize the routes blueprint
routes_bp = Blueprint('routes', __name__)


def init_routes(app):
    from .auth import auth_bp
    from .projects import projects_bp
    from .users import users_bp
    from .generation import generation_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(generation_bp)

