"""Testing the Meal Class
"""
import datetime
import uuid
from flask import json
from tests.test_api import MainTests
from api.auth_helper import get_token
from api.models.meal import Meal
from api.models.menu import Menu
from api.models.orders import Order
from api.models.meal import Database


class OrderTests(MainTests):
    """Order Test
    """

    def test_order_meal(self):
        """Test order meal from today's menu
        """
        Meal.save(self.meal_data)
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        Menu.set_menu(date, self.meal_data)
        response = self.app.post('/api/v1/orders', data=json.dumps({
            'selected_id': self.meal_data['id']
        }))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Order created successfully', response.data)

    def test_get_all_orders(self):
        """Testing retrieval of all orders
        """
        Meal.save(self.meal_data)
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        Menu.set_menu(date, self.meal_data)
        Order.add_order(self.meal_data)
        response = self.app.get('/api/v1/orders')
        self.assertEqual(response.status_code, 200)
