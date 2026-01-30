"""
Church Information System - Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes import auth_bp, main_bp, members_bp, caregroups_bp, settings_bp, admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(caregroups_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(admin_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # Initialize default data
        from app.models import User, CareGroup, Setting, Ministry
        
        # Create default admin if no users exist
        if User.query.first() is None:
            from werkzeug.security import generate_password_hash
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin',
                status='active'
            )
            db.session.add(admin)
            
            # Create default care groups
            default_caregroups = [
                CareGroup(name='Yellow', color='#FFD700', leader_id=None),
                CareGroup(name='Blue', color='#1E90FF', leader_id=None),
                CareGroup(name='Red', color='#DC143C', leader_id=None),
                CareGroup(name='Green', color='#32CD32', leader_id=None),
            ]
            for cg in default_caregroups:
                db.session.add(cg)
            
            # Create default ministries
            default_ministries = [
                Ministry(name='Youth'),
                Ministry(name='Adult'),
                Ministry(name='Choir'),
                Ministry(name='Ladies'),
                Ministry(name='Laymen'),
                Ministry(name='Children'),
            ]
            for ministry in default_ministries:
                db.session.add(ministry)
            
            # Create default settings
            default_settings = [
                Setting(setting_name='church_name', setting_value='Mountain Brook Church'),
                Setting(setting_name='church_address', setting_value=''),
                Setting(setting_name='church_contact', setting_value=''),
                Setting(setting_name='default_theme', setting_value='light'),
                Setting(setting_name='items_per_page', setting_value='10'),
                Setting(setting_name='enable_baptism_field', setting_value='true'),
            ]
            for setting in default_settings:
                db.session.add(setting)
            
            db.session.commit()
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    return app
