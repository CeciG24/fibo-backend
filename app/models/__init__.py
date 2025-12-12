
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""
Models package initialization.

Importa todos los modelos en el orden correcto para evitar dependencias circulares.
"""

# Importar modelos de base de datos en orden de dependencias
from app.models.user import User
from app.models.project import Project, Generation

# Importar dataclasses (no tienen dependencias de DB)
from app.models.camera import CameraSettings
from app.models.lighting import LightingSetup, LightSource
from app.models.scene import Scene

# Exportar todo
__all__ = [
    'User',
    'Project',
    'Generation',
    'CameraSettings',
    'LightingSetup',
    'LightSource',
    'Scene'
]