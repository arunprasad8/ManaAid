from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from datetime import timedelta

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    # Build an absolute path to the instance database and ensure the directory exists
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    instance_dir = os.path.join(project_root, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    db_path = os.path.join(instance_dir, 'mana_aid.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Remember-me cookie duration
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    # csrf.init_app(app)  # Temporarily disabled for simplicity
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.donor import donor_bp
    from app.routes.recipient import recipient_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(donor_bp)
    app.register_blueprint(recipient_bp)
    
    # Import all models to ensure they are registered with SQLAlchemy
    from app.models.user import User
    from app.models.surplus_post import SurplusPost
    from app.models.food_request import FoodRequest
    from app.models.volunteer_task import VolunteerTask
    from app.models.sponsor_order import SponsorOrder
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    return app