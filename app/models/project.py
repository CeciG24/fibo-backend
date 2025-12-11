from datetime import datetime
from . import db
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
    
    # Relaciones
    owner = db.relationship('User', backref=db.backref('projects', lazy='dynamic', cascade='all, delete-orphan'))
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
    
    @classmethod
    def get_all(cls, user_id=None, page=1, per_page=10):
        """
        Obtiene todos los proyectos con paginación.
        Si user_id se proporciona, filtra por usuario.
        """
        query = cls.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        query = query.order_by(cls.updated_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'projects': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }
    
    @classmethod
    def get_by_id(cls, project_id):
        """Obtiene un proyecto por ID"""
        project = cls.query.get(project_id)
        if not project:
            return None
        return project.to_dict(include_generations=True)
    
    @classmethod
    def create(cls, user_id, title, description='', **kwargs):
        """Crea un nuevo proyecto"""
        project = cls(
            user_id=user_id,
            title=title,
            description=description,
            aspect_ratio=kwargs.get('aspect_ratio', '16:9'),
            resolution=kwargs.get('resolution', '1024x576'),
            is_public=kwargs.get('is_public', False)
        )
        
        db.session.add(project)
        db.session.commit()
        
        return project.to_dict()
    
    @classmethod
    def update(cls, project_id, **kwargs):
        """Actualiza un proyecto existente"""
        project = cls.query.get(project_id)
        if not project:
            return None
        
        # Campos actualizables
        allowed_fields = [
            'title', 'description', 'thumbnail_url',
            'aspect_ratio', 'resolution', 'is_public', 'status'
        ]
        
        for field in allowed_fields:
            if field in kwargs:
                setattr(project, field, kwargs[field])
        
        db.session.commit()
        return project.to_dict()
    
    @classmethod
    def delete(cls, project_id):
        """Elimina un proyecto"""
        project = cls.query.get(project_id)
        if not project:
            return False
        
        db.session.delete(project)
        db.session.commit()
        return True
    
    def is_owner(self, user_id):
        """Verifica si un usuario es el dueño del proyecto"""
        return self.user_id == user_id