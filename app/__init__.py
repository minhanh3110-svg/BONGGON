from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import config

# Khởi tạo các extension
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load cấu hình
    app.config.from_object(config[config_name])
    
    # Khởi tạo các extension với app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Cấu hình login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'info'
    
    # Đăng ký các blueprint
    from app.routes import main, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    
    # Đăng ký các filter
    from app.utils import filters
    app.jinja_env.filters.update(filters.custom_filters)
    
    return app 