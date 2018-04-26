"""Main test

"""
import uuid
import unittest
from api.auth_helper import get_token
from api.models.meal import Meal
from api.models.user import User
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
            'email': 'osoticharles@gmail.com',
            'designation': 'caterer',
            'password': 'kulundeng',
            'confirm_password': 'kulundeng'
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
            # User id that will be used to create an orphan token
            orphan_id = uuid.uuid4().hex
            test_user.save({
                'id': orphan_id,
                'username': "victorosoti",
                'email': "kulundeng@gmail.com",
                'designation': self.user_data['designation'],
                'password': self.user_data['password'],
                'confirm_password': self.user_data['confirm_password']
            })
            # Issue a token the the test user (sample_user)
            # Store test token in auth storage auth_token list
            token = get_token(self.user_data['id'])
            # Orphan token: User token that do not have any registered business
            orphan_token = get_token(orphan_id)
            expired_token = get_token(self.user_data['id'], -3600)
            # Create bad signature token
            # Bad signature: #nt secret key from the one used in our API used
            # to hash tokens
            other_signature_token = get_token(
                self.user_data['id'], 3600, 'other_signature')
            User().add_token(token)
            User().add_token(expired_token)
            User().add_token(orphan_token)
            User().add_token(other_signature_token)
            self.test_token = token
            self.expired_test_token = expired_token
            self.other_signature_token = other_signature_token
            self.orphan_test_token = orphan_token



