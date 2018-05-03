import datetime
from time import strftime
import uuid
from functools import wraps
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from ..models.database import Database
from ..models.meal import Meal
from ..models.user import User
from ..models.menu import Menu
from ..models.orders import Order
from ..docs.docs import (
    CREATE_MEAL_DOCS,
    DELETE_MEAL_DOCS,
    GET_MEALS_DOCS, GET_MEAL_DOCS,
    UPDATE_MEAL_DOCS,
    SIGNUP_DOCS,
    SIGNIN_DOCS,
    SIGNOUT_DOCS,
    CREATE_MENU_DOCS,
    GET_MENU_DOCS,
    MAKE_ORDER_DOCS,
    UPDATE_ORDER_DOCS,
    GET_ORDERS_DOCS,
    GET_ORDER_DOCS
)

from ..auth_helper import get_token, token_id

from ..input_utils import (validate, CREATE_MEAL_RULES,
                          USER_SIGNUP_RULES, USER_SIGNIN_RULES)

from flasgger.utils import swag_from

# v1 = Blueprint('v1', __name__, url_prefix='/v1/api')
from . import v1

def login_required(arg):
    """ Decorator to check if a user is logged in """
    @wraps(arg)
    def wrap(*args, **kwargs):
        """Checking if token exists in the request header
        """
        if request.headers.get('Authorization'):
            token = request.headers.get('Authorization')
            if User.token_exists(token) and token_id(token):
                return arg(*args, **kwargs)
        response = jsonify({
            'status': 'error',
            'message': "Unauthorized"
        })
        response.status_code = 401
        return response
    return wrap


def admin_required(arg):
    """ Decorator to check if a user logged in is admin
    """
    @wraps(arg)
    def wrap(*args, **kwargs):
        """Checking if token exists in the request header
        """
        if request.headers.get('Authorization'):
            user_id = token_id(request.headers.get('Authorization'))
            if user_id in [user['id'] for user in Database.users if
                           user['designation'].lower() == "caterer"]:
                return arg(*args, **kwargs)
        response = jsonify({
            'status': 'error',
            'message': "You don't have permission to view this page"
        })
        response.status_code = 403
        return response
    return wrap


@v1.route('/auth/register', methods=['POST'])
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
    data = {
        'id': uuid.uuid4().int,
        'username': input_data['username'],
        'email': input_data['email'],
        'designation': input_data['designation'],
        'password': input_data['password']
    }

    if User.user_already_exists(data['email']):
        response = jsonify({
            'status': 'error',
            'message': 'Sorry. The email you provided has been taken.'
        })
        response.status_code = 400
        return response

    User.save(data)
    response = jsonify({
        'status': 'ok',
        'message':  "You have been successfully registered"
    })
    response.status_code = 201
    return response


@v1.route('/auth/login', methods=['POST'])
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

    data = {
        'email': input_data['email'],
        'password': input_data['password'],
    }

    user_ = User.get_user(data['email'])

    if user_:
        if check_password_hash(user_['password'], data['password']):
            token = get_token(user_['id'])
            User.add_token(token)
            response = jsonify({
                'status': 'ok',
                'message': 'You have successfully logged in',
                'access_token': token,
            })
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
        'message': 'Invalid email or password'
    })
    response.status_code = 400
    return response


@v1.route('/auth/logout', methods=['POST'])
@login_required
@swag_from(SIGNOUT_DOCS)
def logout():
    """Logs the user out by removing the token"""
    Database.remove_token(request.headers.get('Authorization'))
    response = jsonify({
        'status': 'ok',
        'message': "You have successfully logged out"
    })
    response.status_code = 200
    return response


@v1.route('/meals', methods=['POST'])
@swag_from(CREATE_MEAL_DOCS)
# @login_required
# @admin_required
def create_meal():
    """Create a new meal
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
    data = {
        'id': uuid.uuid4().hex,
        'title': input_data['title'],
        'price': input_data['price'],
    }
    if Meal.meal_already_exist(input_data['title']):
        response = jsonify(
            status='error',
            message="You have already submitted a meal with the same title"
        )
        response.status_code = 400
        return response
    Meal.save(data)
    response = jsonify({
        'status': 'ok',
        'message': "Meal has been successfully created"
    })
    response.status_code = 201
    return response


@v1.route('/meals', methods=['GET'])
@swag_from(GET_MEALS_DOCS)
# @admin_required
def get_meals():
    """This function retrieves all meals created by the caterer
    """
    meals = Meal.get_meals()
    if meals:
        response = jsonify({
            'status': 'ok',
            'message': 'There are ' + str(len(meals)) + ' meals',
            'meals': meals
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error',
        message='The are no meals'
    )
    response.status_code = 204
    return response


@v1.route('/meals/<meal_id>', methods=['GET'])
@swag_from(GET_MEAL_DOCS)
# @login_required
# @admin_required
def get_meal(meal_id):
    """Retrieves meal
    """
    if meal_id in [meal['id'] for meal in Database.meals]:
        meal = Meal.get_meal(meal_id)
        response = jsonify({
            'status': 'ok',
            'message': 'Meal Found',
            'meal': meal,
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error',
        message='No meal with that id'
    )
    response.status_code = 400
    return response


@v1.route('/meals/<meal_id>', methods=['PUT'])
@swag_from(UPDATE_MEAL_DOCS)
# @login_required
# @admin_required
def update_meal(meal_id):
    """Update a meal
    """
    input_data = request.get_json(force=True)
    meal = Meal.get_meal(meal_id)
    if meal:
        is_valid = validate(input_data, CREATE_MEAL_RULES)
        if is_valid != True:
            response = jsonify(
                status='error',
                message='Please fill in with valid data',
                errors=is_valid)
            response.status_code = 400
            return response
        data = {
            'title': input_data['title'],
            'price': input_data['price'],
        }

        if Meal.meal_already_exist(input_data['title']):
            response = jsonify(
                status='error',
                message='There is a meal with similar title in the database')
            response.status_code = 400
            return response
        Meal.update(meal_id, data)
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


@v1.route('/meals/<meal_id>', methods=['DELETE'])
@swag_from(DELETE_MEAL_DOCS)
# @login_required
# @admin_required
def delete_meal(meal_id):
    """Delete meal
    """
    meal = Meal.get_meal(meal_id)
    if meal:
        Meal.delete(meal_id)
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


@v1.route('/menu', methods=['POST'])
@swag_from(CREATE_MENU_DOCS)
def create_menu():
    """Set day's menu
    """
    input_data = request.get_json(force=True)
    selected_id = input_data['selected_id']
    if len(selected_id) != 32:
        response = jsonify({
            'status': 'error',
            'message': "Invalid meal id selected"
        })
        response.status_code = 400
        return response
    meal = [meal for meal in Database.meals if meal.get('id') == selected_id]
    if meal:
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        Menu.set_menu(date, meal[0])
        response = jsonify({
            'status': 'ok',
            'message': "Meal has been successfully added to the menu"
        })
        response.status_code = 201
        return response
    response = jsonify({
        'status': 'error',
        'message': "Meal selected not found"
    })
    response.status_code = 400
    return response


@v1.route('/menu', methods=['GET'])
@swag_from(GET_MENU_DOCS)
def get_menu():
    """Get day's menu
    """
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    if date in Database.menu:
        menu_meals = Database.menu[date]
        response = jsonify({
            'status': 'ok',
            'message': "Menu found",
            'date': date,
            'meals': menu_meals
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error',
        message='No menu found'
    )
    response.status_code = 400
    return response


@v1.route('/orders', methods=['GET'])
@swag_from(GET_ORDERS_DOCS)
def get_orders():
    """This function retrieves all orders made by customers
    """
    orders = Database.orders
    if orders:
        response = jsonify({
            'status': 'ok',
            'message': 'There are ' + str(len(orders)) + ' orders',
            'orders': orders
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error',
        message='The are no orders'
    )
    response.status_code = 204
    return response


@v1.route('/orders/<order_id>', methods=['PUT'])
@swag_from(UPDATE_ORDER_DOCS)
def update_order(order_id):
    """Update an order 
    """
    input_data = request.get_json(force=True)
    if order_id in [order['id'] for order in Database.orders]:
        order = Order.get_order(order_id)
        selected_id = input_data['selected_id']
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        new_order = [meal for meal in Database.menu[date]
                     if meal.get('id') == selected_id]
        print(new_order[0])
        if new_order:
            data = {
                'id': order['id'],
                'date': order['date'],
                'time_created': order['time'],
                'time_modified': strftime("%H:%M:%S"),
                'my_order': new_order[0]
            }
            Order.update(order_id, data)
            response = jsonify({
                'status': 'ok',
                'message': "The order has been successfully updated"
            })
            response.status_code = 202
            return response
        response = jsonify({
            'status': 'error',
            'message': "The meal you ordered is not in the menu"
        })
        response.status_code = 400
        return response
    response = jsonify(status='error',
                       message='This order does not exist')
    response.status_code = 400
    return response


@v1.route('/orders/<order_id>', methods=['GET'])
@swag_from(GET_ORDER_DOCS)
def get_order(order_id):
    """get order details 
    """
    # order = [order for order in Database.orders if order.get('id') == order_id]
    if order_id in [order['id'] for order in Database.orders]:
        order = Order.get_order(order_id)
        response = jsonify({
            'status': 'ok',
            'message': "The order has been found",
            'order': order
        })
        response.status_code = 200
        return response
    response = jsonify(status='error',
                       message='This order does not exist')
    response.status_code = 400
    return response


@v1.route('/orders', methods=['POST'])
@swag_from(MAKE_ORDER_DOCS)
def make_order():
    """Make an order
    """
    input_data = request.get_json(force=True)
    selected_id = input_data['selected_id']
    if len(selected_id) != 32:
        response = jsonify({
            'status': 'error',
            'message': "Invalid meal id selected"
        })
        response.status_code = 400
        return response
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        menu_meals = Database.menu[date]
    except KeyError:
        response = jsonify({
            'status': 'error',
            'message': 'The menu has not been set.'
        })
        response.status_code = 400
        return response

    if len(menu_meals) == 0:
        response = jsonify({
            'status': 'error',
            'message': 'The menu has not been set.'
        })
        response.status_code = 400
        return response

    my_order = [meal for meal in menu_meals if meal.get('id') == selected_id]
    if my_order:
        data = {
            'id': uuid.uuid4().hex,
            'date': datetime.datetime.today().strftime('%Y-%m-%d'),
            'time': strftime("%H:%M:%S"),
            'my_order': my_order[0]
        }
        Order.add_order(data)
        response = jsonify({
            'status': 'ok',
            'message': "Order created successfully",
        })
        response.status_code = 201
        return response
    response = jsonify({
        'status': 'ok',
        'message': "No meal with that id",
    })
    response.status_code = 400
    return response


@v1.errorhandler(400)
def bad_request(error):
    '''error handler for Bad request'''
    return jsonify(dict(error='Bad request')), 400


@v1.errorhandler(404)
def page_not_found(error):
    """error handler for 404
    """
    return jsonify(dict(error='Page not found')), 404


@v1.errorhandler(405)
def unauthorized(error):
    """error handler for 405
    """
    return jsonify(dict(error='Method not allowed')), 405


@v1.errorhandler(500)
def internal_server_error(error):
    """error handler for 500
    """
    return jsonify(dict(error='Internal server error')), 500
