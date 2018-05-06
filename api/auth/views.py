import datetime
from flask import Blueprint, request, jsonify
from functools import wraps

from ..models.models import db, User, Forbidden
from api import bcrypt

from ..helpers.input_utils import validate, USER_SIGNUP_RULES, USER_SIGNIN_RULES
from ..helpers.decorators import login_required, admin_required
from ..docs.docs import SIGNUP_DOCS, SIGNIN_DOCS, SIGNOUT_DOCS

from flasgger.utils import swag_from

date = datetime.datetime.today().strftime('%Y-%m-%d')



auth = Blueprint('auth', __name__, url_prefix='/api/v2')

@auth.route('/auth/register', methods=['POST'])
@swag_from(SIGNUP_DOCS)
def register():
    """Register User"""
    is_valid = validate(request.get_json(force=True), USER_SIGNUP_RULES)
    input_data = request.get_json()
    if is_valid != True:
        response = jsonify(
            status='error',
            message="Please provide valid email and password",
            errors=is_valid
        )
        response.status_code = 400
        return response
    user = User.query.filter_by(email=input_data['email']).first()
    if not user:
        user = User(
            username=input_data['username'],
            email=input_data['email'],
            password=input_data['password'],
            designation=input_data['designation'])
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_token(user.id).decode()
        response = jsonify({
            'status': 'success',
            'message': 'You are successfully registered.',
            'auth_token': auth_token
        })
        response.status_code = 201
        return response
    response = jsonify(
        status='error',
        message="Please provide valid email and password",
        errors=is_valid
    )
    response.status_code = 400
    return response    

@auth.route('/auth/login', methods=['POST'])
@swag_from(SIGNIN_DOCS)
def login():
    """Logs registered users in"""
    input_data = request.get_json(force=True)
    is_valid = validate(input_data, USER_SIGNIN_RULES)

    if is_valid != True:
        response = jsonify(
            status='error',
            message="Please provide corrent email or password",
            errors=is_valid
        )
        response.status_code = 400
        return response

    user = User.query.filter_by(email=input_data['email']).first()

    if user and bcrypt.check_password_hash(
        user.password, input_data['password']):
        auth_token = user.encode_token(user.id)
        if auth_token:
            response = jsonify(
                status='ok',
                message='You have successfully logged in',
                auth_token=auth_token.decode()
            )
            response.status_code = 200
            return response
         
        response = jsonify({
            'status': 'error',
            'message': 'Please provide valid password'
        })
        response.status_code = 401
        return response
    response = jsonify({
        'status': 'error',
        'message': 'User does not exist.'
    })
    response.status_code = 404
    return response


@auth.route('/auth/logout', methods=['POST'])
@login_required
@swag_from(SIGNOUT_DOCS)
def logout():
    """Logs the user out"""
    header = request.headers.get('Authorization')
    if header:
        auth_token = header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        user_id = User.decode_token(auth_token)
        if not isinstance(user_id, str):
            forbidden = Forbidden(token=auth_token)
            try:
                db.session.add(forbidden)
                db.session.commit()
                response = jsonify({
                    'status': 'ok',
                    'message': "You have successfully logged out"
                    })
                response.status_code = 200
                return response
            except Exception as e:
                response = jsonify({
                    'status': 'error',
                    'message': e
                    })
                response.status_code = 200
                return response
        else:
            response = jsonify({
                    'status': 'error',
                    'message': user_id})
            response.status_code = 401
            return response      
           
    response = jsonify({
        'status': 'error',
        'message': 'You provided wrong authentication token'        
    })
    response.status_code = 403
    return response
