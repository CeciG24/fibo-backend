class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key_here'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'
    
    # JWT configuration
    JWT_SECRET_KEY = 'your_jwt_secret_key_here'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # FIBO API configuration
    FIBO_API_URL = 'https://api.fibo.com'
    FIBO_API_KEY = 'your_fibo_api_key_here'