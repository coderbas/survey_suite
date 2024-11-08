# backend/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
    
    # Configure the app
    app.config['SECRET_KEY'] = 'Basit@2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Basit%402024@localhost/survey_suite_db?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints and setup routes
    from .routes import routes  # Assuming routes is a Blueprint
    app.register_blueprint(routes)
    
    # Import models to ensure they are registered with SQLAlchemy
    from . import models

    return app
