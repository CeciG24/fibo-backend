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
    FIBO_API_URL = 'https://api.fibo.com'
    FIBO_API_KEY = 'your_fibo_api_key_here'