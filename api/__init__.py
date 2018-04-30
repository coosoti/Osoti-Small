""" Initialize the app 
"""

from flask import Flask
from flasgger import Swagger
from instance.config import app_config

from .views import v1

# app = Flask(__name__, instance_relative_config=True)
# app.register_blueprint(v1)

# import json
# from flask import Flask
# from flask_jwt_extended import JWTManager
# from app.api import api, bam, blacklist
# from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(v1)

    return app

# app.config.from_object('config')