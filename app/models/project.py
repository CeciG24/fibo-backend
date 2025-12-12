from datetime import datetime
from app.models import db
import json

class Project(db.Model):
    __tablename__ = 'projects'
    
    # IDs
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Información básica
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    thumbnail_url = db.Column(db.String(500))
    
    # Configuración del proyecto
    aspect_ratio = db.Column(db.String(20), default='16:9')  # 16:9, 4:3, 1:1, 9:16
    resolution = db.Column(db.String(20), default='1024x576')
    
    # Estado y visibilidad
    is_public = db.Column(db.Boolean, default=False, index=True)
    status = db.Column(db.String(20), default='draft', index=True)  # draft, in_progress, completed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones - Usar strings para evitar import circular
    # owner = relación definida en User via backref
    generations = db.relationship('Generation', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Project {self.id}: {self.title}>'
    
    def to_dict(self, include_generations=False):
        """Serializa el proyecto a diccionario"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'aspect_ratio': self.aspect_ratio,
            'resolution': self.resolution,
            'is_public': self.is_public,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'owner': {
                'id': self.owner.id,
                'username': self.owner.username,
                'avatar_url': self.owner.avatar_url
            }
        }
        
        if include_generations:
            data['generations'] = [g.to_dict() for g in self.generations.order_by('scene_number').all()]
            data['generation_count'] = self.generations.count()
            data['completed_count'] = self.generations.filter_by(status='completed').count()
        
        return data
    
    def is_owner(self, user_id):
        """Verifica si un usuario es el dueño del proyecto"""
        return self.user_id == user_id


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
    
    # Relaciones - user definida en User via backref, project definida arriba
    
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
            'project_id': self.project_id,
            'user_id': self.user_id
        }