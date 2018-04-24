import uuid
from flask import Blueprint, request, jsonify
from .models.database import Database
from .models.meal import Meal
from .models.user import User
from .docs.docs import ( 
    CREATE_MEAL_DOCS,
    DELETE_MEAL_DOCS, 
    GET_MEALS_DOCS, GET_MEAL_DOCS, 
    UPDATE_MEAL_DOCS,
    SIGNUP_DOCS
)

from .input_utils import validate, CREATE_MEAL_RULES, USER_SIGNUP_RULES

from flasgger.utils import swag_from

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')

@v1.route('/auth/register', methods=['POST'])
@swag_from(SIGNUP_DOCS)
def register():
    """This functions enables user registration
    """
    is_valid = validate(request.get_json(force=True), USER_SIGNUP_RULES)
    input_data = request.get_json(force=True)
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
    response =  jsonify(
        status='error',
        message='No meal with that id' 
    )
    response.status_code = 400
    return response

@v1.route('/meals/<meal_id>', methods=['PUT'])
@swag_from(UPDATE_MEAL_DOCS)
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
    response = jsonify(
        status='error',
        message='This meal does not exist or you do have the permission to edit it' 
    )
    response.status_code = 400
    return response    

@v1.route('/meals/<meal_id>', methods=['DELETE'])
@swag_from(DELETE_MEAL_DOCS)
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
    response = jsonify(
        status='error',
        message="This meal does not exist or you do not have the permission to delete it" 
    )
    response.status_code = 400
    return response