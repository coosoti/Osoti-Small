"""Testing the Menu Class
"""
import datetime
import uuid
from flask import json
from api.models import Meal
from tests.main import MainTestCase


class MenuTests(MainTestCase):
    """Main Test
    """

    def test_set_up_menu(self):
        """Test set today's menu 
        """
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef with chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)

            response = self.client.post('v2/api/menu', data=json.dumps({
                'selected_ids': ["1"]
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                b'Menu has been successfully created', response.data)

    def test_set_up_menu_with_invalid_meal_id(self):
        """Test add meal to today's menu with invalid meal id 
        """
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef with chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)
            response = self.client.post('v2/api/menu', data=json.dumps({
                'selected_ids': ["a"]
            }))
            self.assertEqual(response.status_code, 400)


    def test_set_up_menu_with_non_existing_meal_id(self):
        """Test add meal to today's menu with a meal that is not in the meal options 
        """
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef with chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)
            response = self.client.post('v2/api/menu', data=json.dumps({
                'selected_ids': ['5']
            }))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Meal selected not found', response.data)
