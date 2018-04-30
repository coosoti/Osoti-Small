"""Testing the Menu Class
"""
import datetime
import uuid
from flask import json
from tests.test_api import MainTests
from api.auth_helper import get_token
from api.models.meal import Meal
from api.models.database import Database


class MenuTests(MainTests):
    """Main Test
    """
    def test_set_up_menu(self):
        """Test set today's menu 
        """
        Meal.save(self.menu_meal_data)
        response = self.app.post('/api/v1/menu', data=json.dumps({
            'selected_id': self.menu_meal_data['id']
        }))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Meal has been successfully added to the menu', response.data)

    def test_set_up_menu_with_invalid_meal_id(self):
        """Test add meal to today's menu with invalid meal id 
        """
        Meal.save(self.menu_meal_data)
        response = self.app.post('/api/v1/menu', data=json.dumps({
            'selected_id': 'hljjhjhjhl'
        }))
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid meal id selected', response.data)

    def test_set_up_menu_with_non_existing_meal_id(self):
        """Test add meal to today's menu with a meal that is not in the meal options 
        """
        Meal.save(self.menu_meal_data)
        response = self.app.post('/api/v1/menu', data=json.dumps({
            'selected_id': 'abcdefghijklmnopqrstuvwxyzabcdef'
        }))
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Meal selected not found', response.data)
        