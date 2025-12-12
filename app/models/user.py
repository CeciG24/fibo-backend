from flask_bcrypt import Bcrypt
from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    # IDs
    id = db.Column(db.Integer, primary_key=True)
    
    # Credenciales
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Información personal
    full_name = db.Column(db.String(120))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(500))
    country = db.Column(db.String(2))  # Código ISO de 2 letras
    
    # Plan y límites
    plan = db.Column(db.String(20), default='free', index=True)  # free, pro, enterprise
    generations_today = db.Column(db.Integer, default=0)
    total_generations = db.Column(db.Integer, default=0)
    credits = db.Column(db.Integer, default=0)  # Para sistema de créditos opcional
    
    # Estado de cuenta
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_verified = db.Column(db.Boolean, default=False, index=True)
    verification_token = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    last_generation_reset = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones (ya definidas en backref de otros modelos)
    # projects = relationship via backref
    # generations = relationship via backref
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """
        Hash y guarda la contraseña usando bcrypt.
        
        Args:
            password (str): Contraseña en texto plano
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """
        Verifica si la contraseña es correcta.
        
        Args:
            password (str): Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta
        """
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_email=False, include_stats=False):
        """
        Serializa el usuario a diccionario.
        
        Args:
            include_email (bool): Si incluir email (solo para el propio usuario)
            include_stats (bool): Si incluir estadísticas detalladas
            
        Returns:
            dict: Usuario serializado
        """
        data = {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'country': self.country,
            'plan': self.plan,
            'total_generations': self.total_generations,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_email:
            data['email'] = self.email
            data['generations_today'] = self.generations_today
            data['credits'] = self.credits
            data['is_active'] = self.is_active
            data['last_login'] = self.last_login.isoformat() if self.last_login else None
        
        if include_stats:
            from app.models.project import Project, Generation
            data['stats'] = {
                'total_projects': Project.query.filter_by(user_id=self.id).count(),
                'public_projects': Project.query.filter_by(user_id=self.id, is_public=True).count(),
                'completed_generations': Generation.query.filter_by(user_id=self.id, status='completed').count(),
                'favorite_generations': Generation.query.filter_by(user_id=self.id, is_favorite=True).count()
            }
        
        return data
    
    def can_generate(self, max_per_day=None):
        """
        Verifica si el usuario puede generar más imágenes hoy.
        
        Args:
            max_per_day (int, optional): Límite personalizado
            
        Returns:
            bool: True si puede generar
        """
        if self.plan == 'enterprise':
            return True
        
        if max_per_day is None:
            # Límites por plan
            limits = {
                'free': 100,
                'pro': 500,
                'enterprise': float('inf')
            }
            max_per_day = limits.get(self.plan, 100)
        
        return self.generations_today < max_per_day
    
    def get_remaining_generations(self):
        """
        Obtiene el número de generaciones restantes hoy.
        
        Returns:
            int: Generaciones restantes (o 'unlimited')
        """
        if self.plan == 'enterprise':
            return 'unlimited'
        
        limits = {
            'free': 100,
            'pro': 500
        }
        limit = limits.get(self.plan, 100)
        remaining = limit - self.generations_today
        
        return max(0, remaining)
    
    def increment_generation_count(self):
        """
        Incrementa el contador de generaciones.
        Debe llamarse después de cada generación exitosa.
        """
        self.generations_today += 1
        self.total_generations += 1
        db.session.commit()
    
    def reset_daily_count(self):
        """
        Resetea el contador diario de generaciones.
        Debe llamarse con un cronjob cada 24 horas.
        """
        self.generations_today = 0
        self.last_generation_reset = datetime.utcnow()
        db.session.commit()
    
    def spend_credits(self, amount):
        """
        Gasta créditos del usuario.
        
        Args:
            amount (int): Cantidad de créditos a gastar
            
        Returns:
            bool: True si se pudieron gastar, False si no hay suficientes
        """
        if self.credits < amount:
            return False
        
        self.credits -= amount
        db.session.commit()
        return True
    
    def add_credits(self, amount):
        """
        Agrega créditos al usuario.
        
        Args:
            amount (int): Cantidad de créditos a agregar
        """
        self.credits += amount
        db.session.commit()
    
    def upgrade_plan(self, new_plan):
        """
        Actualiza el plan del usuario.
        
        Args:
            new_plan (str): Nuevo plan (free, pro, enterprise)
            
        Returns:
            bool: True si se actualizó exitosamente
        """
        valid_plans = ['free', 'pro', 'enterprise']
        if new_plan not in valid_plans:
            return False
        
        self.plan = new_plan
        db.session.commit()
        return True
    
    def verify_email(self):
        """
        Marca el email como verificado.
        """
        self.is_verified = True
        self.verification_token = None
        db.session.commit()
    
    @classmethod
    def get_by_email(cls, email):
        """
        Busca un usuario por email.
        
        Args:
            email (str): Email del usuario
            
        Returns:
            User: Usuario encontrado o None
        """
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_username(cls, username):
        """
        Busca un usuario por username.
        
        Args:
            username (str): Username del usuario
            
        Returns:
            User: Usuario encontrado o None
        """
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def create(cls, username, email, password, **kwargs):
        """
        Crea un nuevo usuario.
        
        Args:
            username (str): Username único
            email (str): Email único
            password (str): Contraseña en texto plano
            **kwargs: Campos adicionales
            
        Returns:
            User: Usuario creado
        """
        user = cls(
            username=username,
            email=email,
            full_name=kwargs.get('full_name', ''),
            country=kwargs.get('country'),
            plan=kwargs.get('plan', 'free')
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    