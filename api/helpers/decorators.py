import datetime
from flask import Blueprint, request, jsonify
from functools import wraps

from ..models.models import User


def login_required(arg):
    """ Decorator to check if a user is logged in"""
    @wraps(arg)
    def wrap(*args, **kwargs):
        """Checking if token exists in the request header"""
        if request.headers.get('Authorization'):
            auth_token = request.headers.get('Authorization')
            token = auth_token.split(" ")[1]
            resp = User.decode_token(token)
            user = User.query.filter_by(id=resp).first()
            if user:
                return arg(*args, **kwargs)
        response = jsonify({
            'status': 'error',
            'message': "Unauthorized"
        })
        response.status_code = 401
        return response
    return wrap


def admin_required(arg):
    """ Decorator to check if a user is logged in"""
    @wraps(arg)
    def wrap(*args, **kwargs):
        """Checking if token exists in the request header"""
        if request.headers.get('Authorization'):
            auth_token = request.headers.get('Authorization')
            token = auth_token.split(" ")[1]
            resp = User.decode_token(token)
            user = User.query.filter_by(id=resp).first()
            if user.designation.lower() == "caterer":
                return arg(*args, **kwargs)
            response = jsonify({
                'status': 'error',
                'message': "Unauthorized. Login in as an admin"
            })
            response.status_code = 403
            return response
        response = jsonify({
            'status': 'error',
            'message': "Unauthorized. Please Login"
        })
        response.status_code = 403
        return response    
    return wrap
