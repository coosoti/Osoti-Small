from flask import Blueprint
from .models.database import Database
from .models.meal import Meal

from flasgger.utils import swag_from

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')



@api.route('/meals', methods=['POST'])
@swag_from(CREATE_POST_DOCS)
def create_meal():
	"""Create a new meal"""
	input_data = request.get_json(force=True)
	is_valid = validate(input_data, CREATE_POST_RULES)

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
		'message': "Your meal has been successfully created"
	})
	response.status_code = 201
	return response