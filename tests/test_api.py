"""Main test

"""
import uuid
import unittest
from api.auth_helper import get_token
from api.models.meal import Meal
from api.models.user import User
from api import create_app

app = create_app(config_name='testing')


class MainTests(unittest.TestCase):
    """Test for the API
    """

    def setUp(self):
        """Setting up test data
        """
        self.app = app.test_client()
        self.app.testing = True

        self.meal_data = {
            'id': uuid.uuid4().hex,
            'title': 'Beef with rice',
            'price': '600.00'
        }
        self.menu_meal_data = {
            'id': uuid.uuid4().hex,
            'title': 'Beef with rice',
            'price': '600.00'
        }

        self.user_data = {
            'id': uuid.uuid4().hex,
            'username': 'CharlesOsoti',
            'email': 'osoticharles@gmail.com',
            'designation': 'caterer',
            'password': 'kulundeng',
            'confirm_password': 'kulundeng'
        }
        self.orders = {
            'date': '2018-4-25',
            'id': uuid.uuid4().hex,
            'my_order': [
                {
                    'id': uuid.uuid4().hex,
                    'title': 'Beef with rice',
                    'price': '600.00'
                }
            ]
        }

        test_user = User()
        test_user.save({
            'id': self.user_data['id'],
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'designation': self.user_data['designation'],
            'password': self.user_data['password'],
            'confirm_password': self.user_data['confirm_password']
        })

        Meal.save(self.meal_data)
        with app.test_request_context():
            orphan_id = uuid.uuid4().hex
            test_user.save({
                'id': orphan_id,
                'username': "victorosoti",
                'email': "kulundeng@gmail.com",
                'designation': self.user_data['designation'],
                'password': self.user_data['password'],
                'confirm_password': self.user_data['confirm_password']
            })
            token = get_token(self.user_data['id'])
            other_signature_token = get_token(
                self.user_data['id'], 3600, 'other_signature')
            User().add_token(token)
            self.test_token = token
