""" Initialize the app 

"""

from flask import Flask
from flasgger import Swagger

from .views import v1

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(v1)

SWAGGER_CONFIG = {
	"headers": [],
	"title": "Book-A-Meal",
	"specs": [
		{
			"version": "1.0",
			"title": "API Version 1",
			"endpoint": 'apispecs',
			"route": '/api/v1/docs.json',
			"rule_filter": lambda rule: True,
			"model_filter": lambda rule: True,
		}
	],
	"static_url_path": "/swagger_files",
	"swagger_ui": True,
	"specs_route": "/api/v1"	
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

app.config.from_object('config')