import uuid
from flask import Blueprint, request, jsonify
from .models.database import Database
from .models.meal import Meal
from .docs.docs import ( 
    CREATE_MEAL_DOCS, 
    GET_MEALS_DOCS, GET_MEAL_DOCS, 
    UPDATE_MEAL_DOCS
)

from .input_utils import validate, CREATE_MEAL_RULES

from flasgger.utils import swag_from

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')



@v1.route('/meals', methods=['POST'])
@swag_from(CREATE_MEAL_DOCS)
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
def get_meals():
    """This function retrieves all meals created by the caterer
    """
    meals = Meal.get_meals()
    if meals:
        response = jsonify({
            'status': 'ok',
            'message': 'You have ' +str(len(meals)) + ' meals',
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
def get_meal(meal_id):
    """Retrieves a post
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
    response =  jsonify(
        status='error',
        message='No meal with that id' 
    )
    response.status_code = 400
    return response

@v1.route('/meals/<meal_id>', methods=['PUT'])
@swag_from(UPDATE_MEAL_DOCS)
def update_meal(meal_id):
    """Update a meal option
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
    response = jsonify(
        status='error',
        message='This meal does not exist or you do have the permission to edit it' 
    )
    response.status_code = 400
    return response    
