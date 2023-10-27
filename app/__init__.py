from flask import Flask
import os
from .models import db
from .auth import load_user
from flask_login import LoginManager

def create_app():
    """
    Creates a Flask application instance and initializes its configuration settings, database, and login manager.

    Returns:
        app (Flask): A Flask application instance.
    """
    app = Flask(__name__)

    # Set the application's configuration settings
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'yoursecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Load the user
    login_manager.user_loader(load_user)

    # Register blueprints
    from .routes import tasks
    app.register_blueprint(tasks, url_prefix='/api')

    from .web_routes import web
    app.register_blueprint(web)

    from .auth import auth
    app.register_blueprint(auth)

    # Create the database tables
    with app.app_context():
        db.create_all()

    return app




