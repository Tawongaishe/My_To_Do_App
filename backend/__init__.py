from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)


    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'yoursecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import tasks
    app.register_blueprint(tasks, url_prefix='/api')

    from .web_routes import web
    app.register_blueprint(web)

    with app.app_context():
        # Create tables
        db.create_all()

    return app

    # login_manager = LoginManager(app)
