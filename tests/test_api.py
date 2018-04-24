"""Main test

"""
import uuid
import unittest

from api import app

class MainTests(unittest.TestCase):
    """Test for the API
    """
    url_prefix = '/api/v1/'

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
        self.user_data = {
            'id': uuid.uuid4().hex,
            'username': 'CharlesOsoti',
            'email': 'osoticharles.com',
            'password': 'kulundeng',
            'confirm_password': 'kulundeng'
        }



