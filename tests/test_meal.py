"""Testing the Meal Class
"""
import datetime
import uuid
from flask import json
from tests.test_api import MainTests
from api.auth_helper import get_token
from api.models.meal import Meal
from api.models.meal import Database


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

    # testing menu routes
    def test_set_up_menu(self):
        """Test add meal to today's menu list 
        """
        Meal.save(self.meal_data)
        response = self.app.post('/api/v1/menu', data=json.dumps({
            'ids': [self.meal_data['id']]
        }))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Menu has been successfully created', response.data)

    def test_set_up_menu_with_invalid_meal_id(self):
        """Test add meal to today's menu with invalid meal id 
        """
        Meal.save(self.meal_data)
        response = self.app.post('/api/v1/menu', data=json.dumps({
            'ids': ['hljjhjhjhl']
        }))
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid meal id selected', response.data)

    def test_set_up_menu_with_non_existing_meal_id(self):
        """Test add meal to today's menu with a meal that is not in the meal options 
        """
        Meal.save(self.meal_data)
        response = self.app.post('/api/v1/menu', data=json.dumps({
            'ids': ['abcdefghijklmnopqrstuvwxyzabcdef']
        }))
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Meal selected not found', response.data)

    def test_order_meal(self):
        """Test order meal from today's menu
        """
        Meal.save(self.meal_data)
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        Database.set_menu(date, self.meal_data)
        response = self.app.post('/api/v1/orders', data=json.dumps({
            'id': uuid.uuid4().hex,
            'orders_data': self.meal_data
        }))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'You have successfully ordered a meal', response.data)

    def test_update_order(self):
        """Testing meal update function
        """
        new_menu_meal = {
            'title': 'Chicken with Ugali',
            'price': '1000.00'
        }
        Database.orders.append(self.orders_data)
        response = self.app.put('/api/v1/menu/' + self.orders_data['id'],
                                data=json.dumps(new_menu_meal))
        self.assertEqual(response.status_code, 202)
        self.assertIn(
            b'The order has been successfully updated', response.data)

    def test_get_all_orders(self):
        """Testing retrieval of all orders
        """
        response = self.app.get('/api/v1/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'There are 5 orders', response.data)
