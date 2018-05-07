"""Views for menu"""
import datetime
from flask import Blueprint, request, jsonify
from ..models.models import db, Meal, Menu
from ..docs.docs import CREATE_MENU_DOCS, GET_MENU_DOCS
from ..helpers.decorators import login_required, admin_required
from flasgger.utils import swag_from

date = datetime.datetime.today().strftime('%Y-%m-%d')

menus = Blueprint('menu', __name__, url_prefix='/api/v2')


@menus.route('/menu', methods=['POST'])
@admin_required
@swag_from(CREATE_MENU_DOCS)
def create_menu():
    """Create Menu"""
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

    for meal_id in meal_ids:
        if not meal_id.isdigit():
            response = jsonify({
                'status': 'error',
                'message': "Meal id selected is not valid"
            })
            response.status_code = 400
            return response

        meal = Meal.query.filter_by(id=meal_id).first()
        if not meal:
            response = jsonify({
                'status': 'error',
                'message': "Meal selected not found"
            })
            response.status_code = 400
            return response
        menu.meals.append(meal)
    db.session.add(menu)
    db.session.commit()
    response = jsonify({
        'status': 'ok',
        'message': "Menu has been successfully created"
    })
    response.status_code = 201
    return response


@menus.route('/menu', methods=['GET'])
@login_required
@swag_from(GET_MENU_DOCS)
def v2_get_menu():
    """Get Menu"""
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
            'date': date,
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
