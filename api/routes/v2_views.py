import datetime
import itertools
from flask import Blueprint, request, make_response, jsonify
from functools import wraps

from ..models import db, Meal, Menu, User, BlacklistToken
from api import bcrypt

from ..input_utils import (validate, CREATE_MEAL_RULES, USER_SIGNUP_RULES, USER_SIGNIN_RULES)
from ..docs.docs import (
    CREATE_MEAL_DOCS, GET_MEALS_DOCS, 
    GET_MEAL_DOCS, UPDATE_MEAL_DOCS, DELETE_MEAL_DOCS,
    CREATE_MENU_DOCS, GET_MENU_DOCS, SIGNUP_DOCS,
    SIGNIN_DOCS, SIGNOUT_DOCS)

from flasgger.utils import swag_from


v2 = Blueprint('v2', __name__, url_prefix='/v2/api')

def login_required(arg):
    """ Decorator to check if a user is logged in """
    @wraps(arg)
    def wrap(*args, **kwargs):
        """Checking if token exists in the request header
        """
        if request.headers.get('Authorization'):
            auth_token = request.headers.get('Authorization')
            token = auth_token.split(" ")[1]
            resp = User.decode_auth_token(token)
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


@v2.route('/auth/register', methods=['POST'])
@swag_from(SIGNUP_DOCS)
def register():
    """This functions enables user registration
    """
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
        # insert the user
        db.session.add(user)
        db.session.commit()
        # generate the auth token
        auth_token = user.encode_auth_token(user.id).decode()
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

@v2.route('/auth/login', methods=['POST'])
@swag_from(SIGNIN_DOCS)
def login():
    """This functions allows registered users to login"""
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
        auth_token = user.encode_auth_token(user.id)
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


@v2.route('/auth/logout', methods=['POST'])
@login_required
@swag_from(SIGNOUT_DOCS)
def logout():
    """Logs the user out by removing the token"""
    header = request.headers.get('Authorization')
    if header:
        auth_token = header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        user_id = User.decode_auth_token(auth_token)
        if isinstance(user_id, int):
            blacklisted_token = BlacklistToken(token=auth_token)
            try:
                db.session.add(blacklisted_token)
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


@v2.route('/meals', methods=['POST'])
# @login_required
@swag_from(CREATE_MEAL_DOCS)
def v2_create_meal():
    """Create a New Meal
    """
    input_data = request.get_json(force=True)
    is_valid = validate(input_data, CREATE_MEAL_RULES)
    if is_valid != True:
        response = jsonify(
            status='error',
            message='Please fill in with valid data',
            errors=is_valid)
        response.status_code = 400
        return response

    new_meal= Meal(title=input_data['title'], price=input_data['price'])

    if Meal.meal_already_exist(title=input_data['title']):
        response = jsonify(
            status='error',
            message="You have already submitted a meal with the same title"
        )
        response.status_code = 400
        return response
    Meal.save(new_meal)
    response = jsonify({
        'status': 'ok',
        'message': "Meal has been successfully created"
    })
    response.status_code = 201
    return response


@v2.route('/meals', methods=['GET'])
@swag_from(GET_MEALS_DOCS)
# @admin_required
def v2_get_meals():
    """This function retrieves all meals created by the caterer
    """
    data = Meal.get_all()
    meals = []
    if data:       
        for meal in data:
            obj = {
                'id': meal.id,
                'title': meal.title,
                'price': meal.price
            }
            meals.append(obj)   
        response = jsonify({
            'status': 'ok',
            'message': 'There are ' + str(len(meals)) + ' meals',
            'data': [meals]
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error',
        message='The are no meals'
    )
    response.status_code = 204
    return response    

@v2.route('/meals/<meal_id>', methods=['GET'])
@swag_from(GET_MEAL_DOCS)
# @login_required
# @admin_required
def v2_get_meal(meal_id):
    """Retrieves meal"""
    meal = Meal.query.filter_by(id=meal_id).first()
 
    if meal:
        obj = {
            'id': meal.id,
            'title': meal.title,
            'price': meal.price
        }             
        response = jsonify({
            'status': 'ok',
            'message': 'Meal datails',
            'data': [obj]
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error',
        message='No meal with that id'
    )
    response.status_code = 400
    return response


@v2.route('/meals/<meal_id>', methods=['PUT'])
@swag_from(UPDATE_MEAL_DOCS)
# @login_required
# @admin_required
def v2_update_meal(meal_id):
    """Update a meal"""
    input_data = request.get_json(force=True)
    meal = Meal.query.filter_by(id=meal_id).first()
    if meal:
        is_valid = validate(input_data, CREATE_MEAL_RULES)
        if is_valid != True:
            response = jsonify(
                status='error',
                message='Please fill in with valid data',
                errors=is_valid)
            response.status_code = 400
            return response
        meal.title= input_data['title'],
        meal.price = input_data['price']
        # if Meal.meal_already_exist(meal.title) is True:
        #     response = jsonify(
        #         status='error',
        #         message='There is a meal with similar title in the database')
        #     response.status_code = 400
        #     return response
        db.session.commit()
        response = jsonify({
            'status': 'ok',
            'message': "The meal has been successfully updated"
        })
        response.status_code = 202
        return response
    response = jsonify(status='error',
                       message='This meal does not exist or you do have the permission to edit it')
    response.status_code = 400
    return response


@v2.route('/meals/<meal_id>', methods=['DELETE'])
@swag_from(DELETE_MEAL_DOCS)
# @login_required
# @admin_required
def v2_delete_meal(meal_id):
    """Delete meal
    """
    meal = Meal.query.filter_by(id=meal_id).first()
    if meal:
        Meal.delete(meal)
        response = jsonify({
            'status': 'ok',
            'message': "Meal has been successfully deleted"
        })
        response.status_code = 202
        return response
    response = jsonify(status='error',
                       message="This meal does not exist or you do not have the permission to delete it")
    response.status_code = 400
    return response    


# @v2.route('/menu', methods=['POST'])
# @swag_from(CREATE_MENU_DOCS)
# def v2_create_menu():
#     """Set up menu"""
#     date = datetime.datetime.today().strftime('%Y-%m-%d')      
#     new_menu = Menu(date=date)
#     db.session.add(new_menu)
#     db.session.commit()  
#     input_data = request.get_json(force=True)
#     selected_id = input_data['selected_id']
#     if not selected_id.isdigit():
#         response = jsonify({
#             'status': 'error',
#             'message': "Invalid meal id selected"
#         })
#         response.status_code = 400
#         return response
#     meal = Meal.query.filter_by(id=selected_id).first()
#     if meal:
#         new_menu.menu_meals.append(meal)
#         db.session.commit()
#         response = jsonify({
#             'status': 'ok',
#             'message': "Meal has been successfully added to the menu"
#         })
#         response.status_code = 201
#         return response
#     response = jsonify({
#         'status': 'error',
#         'message': "Meal selected not found"
#     })
#     response.status_code = 400
#     return response

# @v2.route('/menu', methods=['GET'])
# @swag_from(GET_MENU_DOCS)
# def v2_get_menu():
#     """Get day's menu"""
#     menu_meals = db.engine.execute("SELECT meal_id FROM menu_meals;")
     
#     meals = []
#     for m_id in menu_meals:
#         meals.append(list(m_id))
#     meal_ids = list(itertools.chain(*meals)) 
#     menu_meals = [Meal.query.filter_by(id=id).one() for id in meal_ids]
#     if menu_meals:
#         all_menu_meals = []   
#         for meal in menu_meals:
#             obj = {
#                 'id': meal.id,
#                 'title': meal.title,
#                 'price': meal.price
#             }
#             all_menu_meals.append(obj)
#         response = jsonify({
#             'status': 'ok',
#             'date': datetime.datetime.today().strftime('%Y-%m-%d'),
#             'message': 'There are ' + str(len(menu_meals)) + ' meals',
#             'meals': all_menu_meals
#         })
#         response.status_code = 200
#         return response 
#     response = jsonify(
#         status='error',
#         message='No menu found'
#         # data=today_menu.meals
#     )
#     response.status_code = 400
#     return response

@v2.route('/menu', methods=['POST'])
@swag_from(CREATE_MENU_DOCS)
def v2_create_menu():
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    menu = Menu.query.filter_by(date=date).first()
    input_data = request.get_json(force=True)    
    if menu:
        response = jsonify({
            'status': 'error',
            'message': "Today's Menu has already been created"
        })
        response.status_code = 400
        return response

    menu = Menu(date=date)
    meal_ids = input_data['selected_ids']

    for meal_id in  meal_ids:
        meal = Meal.query.filter_by(id=meal_id).first()
        menu.meals.append(meal)
    db.session.add(menu)
    db.session.commit()
    response = jsonify({
        'status': 'ok',
        'message': "Menu have successfully been created"
    })
    response.status_code = 200
    return response

@v2.route('/menu', methods=['GET'])
@swag_from(GET_MENU_DOCS)
def v2_get_menu():
    """Get day's menu"""
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    menu = Menu.query.filter_by(date=date).first()
    meals = []
    if menu:       
        for meal in menu.meals:
            obj = {
                'id': meal.id,
                'title': meal.title,
                'price': meal.price
            }
            meals.append(obj)   
        response = jsonify({
            'status': 'ok',
            'message': 'There are ' + str(len(meals)) + ' meals in this menu',
            'data': date,
            'data': [meals]
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error',
        message='The are no meals'
    )
    response.status_code = 204
    return response    



@v2.errorhandler(400)
def bad_request(error):
    '''error handler for Bad request'''
    return jsonify(dict(error='Bad request')), 400


@v2.errorhandler(404)
def page_not_found(error):
    """error handler for 404
    """
    return jsonify(dict(error='Page not found')), 404


@v2.errorhandler(405)
def unauthorized(error):
    """error handler for 405
    """
    return jsonify(dict(error='Method not allowed')), 405


@v2.errorhandler(500)
def internal_server_error(error):
    """error handler for 500
    """
    return jsonify(dict(error='Internal server error')), 500   
