""" Main file for running the app 
"""
import os

from flasgger import Swagger

from api import create_app

config_name = os.getenv('MODE')
app = create_app(config_name)


SWAGGER_CONFIG = {
    "headers": [],
    "title": "Book-A-Meal",
    "specs": [
        {
            "version": "1.0",
            "title": "API Version 1",
            "endpoint": 'apispecs',
            # "route": '/api/v1/docs.json',
             "route": '/api/v2/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda rule: True,
        }
    ],
    "static_url_path": "/swagger_files",
    "swagger_ui": True,
    "specs_route": "/docs"
    # "specs_route": "/api/v2"
}
TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Book-A-Meal",
        "description": "Book-A-Meal API version 1.0",
        "version": "1.0"
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


if __name__ == '__main__':
    app.run()   
