""" Initialize the app 
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from .views import v1
from .v2_views import v2

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    SQLALCHEMY_ECHO = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(v1)
    app.register_blueprint(v2)

    return app
    
