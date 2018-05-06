import os

from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flasgger import Swagger

config_name = os.getenv('MODE')

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

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

@app.errorhandler(400)
def bad_request(error):
    '''error handler for Bad request'''
    return jsonify(dict(error='Bad request')), 400 

@app.errorhandler(404)
def page_not_found(error):
    """error handler for 404
    """
    return jsonify(dict(error='Page not found')), 404


@app.errorhandler(405)
def unauthorized(error):
    """error handler for 405
    """
    return jsonify(dict(error='Method not allowed')), 405


@app.errorhandler(500)
def internal_server_error(error):
    """error handler for 500
    """
    return jsonify(dict(error='Internal server error')), 500



bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from api.meals.views import meals
from api.menu.views import menu
from api.auth.views import auth
from api.orders.views import orders

app.register_blueprint(meals)
app.register_blueprint(menu)
app.register_blueprint(auth)
app.register_blueprint(orders)
