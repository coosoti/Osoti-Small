"""Testing the Meal Class
"""
import uuid
import datetime
from flask import json
from tests.test_api import MainTests
from api.auth_helper import get_token
from api.models.meal import Meal
from api.models.database import Database 


class MealTests(MainTests):
    """Main Test
    """

    def test_create_meal(self):
        """Testing meal creation
        """
        response = self.app.post('/api/v1/meals', data=json.dumps({
            'id': uuid.uuid4().hex,
            'title': 'Beef with chapati',
            'price': '600.00'
        }), headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Meal has been successfully created', response.data)
        

    def test_get_all_meals(self):
        """Testing retrieval of all meals
        """
        Meal.save(self.meal_data)
        response = self.app.get('/api/v1/meals',
                                headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 200)

    def test_get_meal(self):
        """Test retrieve meal details
        """
        Meal.save(self.meal_data)
        response = self.app.get('/api/v1/meals/' + self.meal_data['id'],
                                headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Meal Found', response.data)


    def test_duplicate_attempts(self):
        """Testing attempt to create a duplicate meal
        """
        Meal().save(self.meal_data)
        response = self.app.post('/api/v1/meals',
                                 data=json.dumps(self.meal_data),
                                 headers={'Authorization': self.test_token},
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'You have already submitted a meal with the same title', response.data)

    def test_invalid_or_empty_data_input(self):
        """Testing attempt to create meal with invalid data
        """
        response = self.app.post('/api/v1/meals', data=json.dumps({
            'title': 'Beef with Chicken',
        }), headers={'Authorization': self.test_token},
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please fill in with valid data', response.data)


    def test_delete_meal(self):
        """Testing delete function
        """
        Meal.save(self.meal_data)
        response = self.app.delete('/api/v1/meals/' + self.meal_data['id'],
                                   data={}, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 202)
        self.assertIn(b'Meal has been successfully deleted', response.data)


    def test_update_meal(self):
        """Testing meal update function
        """
        new_data = {
            'title': 'Chicken with Ugali',
            'price': '1000.00'
        }
        Meal.save(self.meal_data)
        response = self.app.put('/api/v1/meals/' + self.meal_data['id'],
                                data=json.dumps(new_data),
                                headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 202)
        self.assertIn(b'The meal has been successfully updated', response.data)
