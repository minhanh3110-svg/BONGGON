import os
from datetime import timedelta

class Config:
    # Cấu hình cơ bản
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-should-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cấu hình database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db'
    
    # Cấu hình upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Cấu hình session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Cấu hình mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    
    # Trong production nên sử dụng biến môi trường cho SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Cấu hình SSL/TLS
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 