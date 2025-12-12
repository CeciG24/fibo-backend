from datetime import datetime
import json
from . import db
from .project import Project
from .user import User

class Generation(db.Model):
    __tablename__ = 'generations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, index=True)
    
    # Prompt y resultado
    prompt = db.Column(db.Text, nullable=False)
    negative_prompt = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    
    # Parámetros guardados (JSON)
    parameters = db.Column(db.Text)  # JSON string con todos los parámetros
    
    # Metadatos
    seed = db.Column(db.Integer)
    generation_time = db.Column(db.Float)  # Tiempo en segundos
    fibo_generation_id = db.Column(db.String(100))  # ID de FIBO
    
    # Estado
    status = db.Column(db.String(20), default='pending', index=True)  # pending, generating, completed, failed
    error_message = db.Column(db.Text)
    
    # Organización
    scene_number = db.Column(db.Integer)
    is_favorite = db.Column(db.Boolean, default=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime)
    
    # Relaciones
    user = db.relationship('User', backref=db.backref('generations', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Generation {self.id} - {self.status}>'
    
    def set_parameters(self, params_dict):
        """Guarda los parámetros como JSON"""
        self.parameters = json.dumps(params_dict)
    
    def get_parameters(self):
        """Obtiene los parámetros desde JSON"""
        if self.parameters:
            return json.loads(self.parameters)
        return {}
    
    def to_dict(self):
        """Serializa la generación a diccionario"""
        return {
            'id': self.id,
            'prompt': self.prompt,
            'negative_prompt': self.negative_prompt,
            'image_url': self.image_url,
            'parameters': self.get_parameters(),
            'seed': self.seed,
            'generation_time': self.generation_time,
            'status': self.status,
            'error_message': self.error_message,
            'scene_number': self.scene_number,
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'project_id': self.project_id
        }