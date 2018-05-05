import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flasgger import Swagger

config_name = os.getenv('MODE')

app = Flask(__name__)

app.config.from_object(app_config[config_name])

SWAGGER_CONFIG = {
    "headers": [],
    "title": "Book-A-Meal",
    "specs": [
        {
            "version": "1.0",
            "title": "API Version 1",
            "endpoint": 'apispecs',
            "route": '/api/v2/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tags: True,
        }
    ],
    "static_url_path": "/swagger_files",
    "swagger_ui": True,
    "specs_route": "/docs"
}
TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Book-A-Meal",
        "description": "Book-A-Meal API version 2.0",
        "version": "2.0"
    },
    "consumes": [
        "application/json",
    ],
    "produces": [
        "application/json",
    ],
    "schemes": [
        "http",
        "https"
    ],
    "operationId": "getmyData"
}


SWAGGER = Swagger(app, config=SWAGGER_CONFIG, template=TEMPLATE) 



bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from api.routes.v2_views import v2
app.register_blueprint(v2)