from flask import Blueprint

v1 = Blueprint('v1', __name__, url_prefix='/v1/api')
v2 = Blueprint('v2', __name__, url_prefix='/v2/api')
# api = Blueprint('api', __name__, url_prefix='/api')
