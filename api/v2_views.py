from flask import Blueprint, request, jsonify

v2 = Blueprint('v2', __name__, url_prefix='/api/v2')