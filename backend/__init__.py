from flask import Flask
from .auth import load_user
from flask_login import LoginManager
import os
from .models import Users, db


def create_app():

    app = Flask(__name__)


    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'yoursecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@your-database-instance.amazonaws.com/your-database-name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

     # Assign the user loader function
    login_manager.user_loader(load_user)

    #register blueprints
    from .routes import tasks
    app.register_blueprint(tasks, url_prefix='/api')

    from .web_routes import web
    app.register_blueprint(web)

    from .auth import auth
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    return app

    # login_manager = LoginManager(app)


