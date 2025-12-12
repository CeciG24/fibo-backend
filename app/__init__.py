from flask import Flask
from .config import Config
from models import db
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from .routes import init_routes
        init_routes(app)

    return app