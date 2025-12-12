class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key_here'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://fibodb_jj0j_user:vFGY83RK2fanHeoDt3XyIWtCWlUEzSp0'
        '@dpg-d4to2qmmcj7s7383oa7g-a.oregon-postgres.render.com/fibodb_jj0j'
    )
    
    # JWT configuration
    JWT_SECRET_KEY = 'your_jwt_secret_key_here'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # FIBO API configuration
    FIBO_API_URL = 'https://engine.prod.bria-api.com/v2'
    FIBO_API_KEY = 'f7b5e814d48a4544b18433faabc6587d'

    # Mock mode
    FIBO_MOCK_MODE = False
    # Storage
    UPLOAD_FOLDER = './uploads'
    OUTPUT_FOLDER = './outputs'
    MAX_CONTENT_LENGTH = 16777216