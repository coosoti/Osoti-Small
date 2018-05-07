"""Meal Views"""
from flask import Blueprint, request, jsonify
from ..models.models import db, Meal
from ..docs.docs import (
    CREATE_MEAL_DOCS, GET_MEALS_DOCS,
    GET_MEAL_DOCS, UPDATE_MEAL_DOCS, DELETE_MEAL_DOCS)
from flasgger.utils import swag_from
from ..helpers.input_utils import validate, CREATE_MEAL_RULES
from ..helpers.decorators import admin_required

meals = Blueprint('meals', __name__, url_prefix='/api/v2')


@meals.route('/meals', methods=['POST'])
@admin_required
@swag_from(CREATE_MEAL_DOCS)
def create_meal():
    """Create a New Meal"""
    input_data = request.get_json(force=True)
    is_valid = validate(input_data, CREATE_MEAL_RULES)
    if is_valid != True:
        response = jsonify(
            status='error',
            message='Please fill in with valid data',
            errors=is_valid)
        response.status_code = 400
        return response

    new_meal = Meal(title=input_data['title'], price=input_data['price'])

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


@meals.route('/meals', methods=['GET'])
@swag_from(GET_MEALS_DOCS)
@admin_required
def get_meals():
    """Retrieves all meal options"""
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


@meals.route('/meals/<meal_id>', methods=['GET'])
@swag_from(GET_MEAL_DOCS)
@admin_required
def get_meal(meal_id):
    """Retrieves meal detail"""
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


@meals.route('/meals/<meal_id>', methods=['PUT'])
@swag_from(UPDATE_MEAL_DOCS)
@admin_required
def update_meal(meal_id):
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
        meal.title = input_data['title'],
        meal.price = input_data['price']
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


@meals.route('/meals/<meal_id>', methods=['DELETE'])
@swag_from(DELETE_MEAL_DOCS)
@admin_required
def delete_meal(meal_id):
    """Delete meal"""
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
