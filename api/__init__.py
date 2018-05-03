""" Initialize the app 
"""
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from .routes.views import v1
# from .routes.v2_views import v2


db = SQLAlchemy()

# from .v2_models.meal import db

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.register_blueprint(v2)
    app.register_blueprint(v1)
    db.init_app(app)

    return app
    
