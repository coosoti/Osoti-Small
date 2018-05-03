import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from instance.config import app_config

config_name = os.getenv('MODE')

app = Flask(__name__)
CORS(app)

app.config.from_object(app_config[config_name])

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from api.routes.v2_views import v2
app.register_blueprint(v2)