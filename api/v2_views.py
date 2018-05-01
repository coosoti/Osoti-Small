from flask import Blueprint, request, jsonify

from .v2_models.meal import Meal

from .input_utils import (validate, CREATE_MEAL_RULES)
from .docs.docs import (
    CREATE_MEAL_DOCS)

from flasgger.utils import swag_from


v2 = Blueprint('v2', __name__, url_prefix='/api/v2')

@v2.route('/meals', methods=['POST'])
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
        'title': input_data['title'],
        'price': input_data['price'],
    }
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