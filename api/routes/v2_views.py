import datetime
from flask import Blueprint, request, jsonify

from ..v2_models.meal import Meal, db, Menu

from ..input_utils import (validate, CREATE_MEAL_RULES)
from ..docs.docs import (
    CREATE_MEAL_DOCS, GET_MEALS_DOCS, 
    GET_MEAL_DOCS, UPDATE_MEAL_DOCS, DELETE_MEAL_DOCS,
    CREATE_MENU_DOCS)

from flasgger.utils import swag_from
import psycopg2


v2 = Blueprint('v2', __name__, url_prefix='/v2/api')

@v2.route('/meals', methods=['POST'])
@swag_from(CREATE_MEAL_DOCS)
def v2_create_meal():
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

@v2.route('/meals/<meal_id>', methods=['GET'])
@swag_from(GET_MEAL_DOCS)
# @login_required
# @admin_required
def v2_get_meal(meal_id):
    """Retrieves meal
    """
    meal = Meal.query.filter_by(id=meal_id).first()
 
    if meal:
        response = jsonify({
            'id': meal.id,
            'title': meal.title,
            'price': meal.price
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
    """Update a meal
    """
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
        if Meal.meal_already_exist(meal.title):
            response = jsonify(
                status='error',
                message='There is a meal with similar title in the database')
            response.status_code = 400
            return response
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


@v2.route('/menu', methods=['POST'])
@swag_from(CREATE_MENU_DOCS)
def v2_create_menu():
    """Set day's menu
    """
    input_data = request.get_json(force=True)
    selected_id = input_data['selected_id']
    # if len(selected_id) != 32:
    #     response = jsonify({
    #         'status': 'error',
    #         'message': "Invalid meal id selected"
    #     })
    #     response.status_code = 400
    #     return response
    meal = Meal.query.filter_by(id=selected_id) #[meal for meal in Database.meals if meal.get('id') == selected_id]
    if meal:
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        new_menu_item = Menu(date=date, meals_id=selected_id)
        # Menu.set_menu(new_menu_item)
        db.session.add(new_menu_item)
        db.session.commit()
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
