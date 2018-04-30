""" Initialize the app 
"""

from flask import Flask
from instance.config import app_config
from .views import v1


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(v1)

    return app
    
