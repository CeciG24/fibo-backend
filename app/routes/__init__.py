from flask import Blueprint

# Initialize the routes blueprint
routes_bp = Blueprint('routes', __name__)

# Import routes to register them with the blueprint
from .auth import *
from .users import *
from .generation import *
from .presets import *
from .projects import *