import datetime
from flask import Blueprint, request, jsonify

from ..models.models import db, Meal, Menu, User, Order

from ..docs.docs import (MAKE_ORDER_DOCS, GET_ORDERS_DOCS,
                         GET_ORDER_DOCS, UPDATE_ORDER_DOCS)
from ..helpers.decorators import login_required, admin_required
from flasgger.utils import swag_from

date = datetime.datetime.today().strftime('%Y-%m-%d')

orders = Blueprint('orders', __name__, url_prefix='/api/v2')


@orders.route('/orders', methods=['POST'])
@swag_from(MAKE_ORDER_DOCS)
def make_order():
    """Make an order"""
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    menu = Menu.query.filter_by(date=date).first()
    input_data = request.get_json(force=True)
    selected_meal_id = input_data['selected_meal_id']
    meal_ids = []
    for meal in menu.meals:
        meal_ids.append(meal.id)
    for selected_meal_id in meal_ids:
        meal = Order(meal_id=selected_meal_id)
        Order.save(meal)
        response = jsonify({
            'status': 'ok',
            'message': 'You order is successfull',
            'date': date
        })
        response.status_code = 201
        return response

    return jsonify(dict(error='The meal is not found')), 400


@orders.route('/orders', methods=['GET'])
@swag_from(GET_ORDERS_DOCS)
def get_orders():
    """Retrieves all orders by customers
    """
    data = Order.get_all()
    orders = []
    if data:
        for order in data:
            meal = Meal.query.filter_by(id=order.meal_id).first()
            data = {
                'id': meal.id,
                'title': meal.title,
                'price': meal.price
            }
            obj = {
                'id': order.id,
                'created ': order.date_created,
                'modified': order.date_modified,
                'order': data
            }
            orders.append(obj)
        response = jsonify({
            'status': 'ok',
            'message': 'There are ' + str(len(orders)) + ' orders',
            'data': orders
        })
        response.status_code = 200
        return response
    response = jsonify(
        status='error',
        message='The are no orders'
    )
    response.status_code = 204
    return response


@orders.route('/orders/<order_id>', methods=['GET'])
@swag_from(GET_ORDER_DOCS)
def get_order(order_id):
    """get order details 
    """
    order = Order.query.get_or_404(order_id)
    if order:
        meal = Meal.query.filter_by(id=order.meal_id).first()
        data = {
            'id': meal.id,
            'title': meal.title,
            'price': meal.price
        }
        response = jsonify({
            'status': 'ok',
            'message': "The order has been found",
            'id': order.id,
            'created ': order.date_created,
            'order': [data]
        })
        response.status_code = 200
        return response
    response = jsonify(status='error',
                       message='This order does not exist')
    response.status_code = 400
    return response


@orders.route('/orders/<order_id>', methods=['PUT'])
@swag_from(UPDATE_ORDER_DOCS)
def update_order(order_id):
    """Modify an Order"""
    order = Order.query.get_or_404(order_id)
    if order:
        menu = Menu.query.filter_by(date=date).first()
        input_data = request.get_json(force=True)
        selected_meal_id = input_data['selected_meal_id']
        meal_ids = []
        for meal in menu.meals:
            meal_ids.append(meal.id)
        for selected_meal_id in meal_ids:
            order.meal_id = selected_meal_id
            db.session.commit()
            response = jsonify({
                'status': 'ok',
                'message': 'You have updated your order successfully'
            })
            response.status_code = 200
            return response
    response = jsonify(status='error',
                       message='This order does not exist')
    response.status_code = 400
    return response


@orders.errorhandler(400)
def bad_request(error):
    '''error handler for Bad request'''
    return jsonify(dict(error='Bad request')), 400


@orders.errorhandler(404)
def page_not_found(error):
    """error handler for 404
    """
    return jsonify(dict(error='Page not found')), 404


@orders.errorhandler(405)
def unauthorized(error):
    """error handler for 405
    """
    return jsonify(dict(error='Method not allowed')), 405


@orders.errorhandler(500)
def internal_server_error(error):
    """error handler for 500
    """
    return jsonify(dict(error='Internal server error')), 500
