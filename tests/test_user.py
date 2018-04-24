"""
    User test Class
"""
import unittest
import uuid
from flask import json
from api.models.user import User
from api.models.meal import Meal
from tests.test_api import MainTests


class UserTests(MainTests):

    def test_user_registration(self):
        """Testing user registration
        """
        response = self.app.post('/api/v1/auth/register', data=json.dumps({
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password': self.user_data['password'],
            'confirm_password': self.user_data['confirm_password']
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'You have been successfully registered', response.data)

    def test_exist_email(self):
        """Testing registration with exist email
        """
        response = self.app.post('/api/v1/auth/register', data=json.dumps({
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password': self.user_data['password'],
            'confirm_password': self.user_data['confirm_password']
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Sorry the email address already exist', response.data)

    def test_login(self):
        """Testing login
        """
        response = self.app.post('/api/v1/auth/login', data=json.dumps({
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been successfully logged in', response.data)

    def test_invalid_credentials_input(self):
        """Testing for invalid credentials
        """
        response = self.app.post('/api/v1/auth/login', data=json.dumps({
            'email': 'osoticharles',
            'password': 'we'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid email or password', response.data)

    def test_logout(self):
        """Test Logout method
        """
        response = self.app.post('/api/v1/auth/logout', data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully logged out', response.data)

    def test_validators_methods(self):
        """Test validators methods
        """
        response = self.app.post('/api/v1/auth/register', data=json.dumps({
            'username': '',
            'email': 'osoti',
            'password': 'afb',
            'confirm_password': 'kulundeng'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid email address', response.data)
        self.assertIn(b'should be string', response.data)
        self.assertIn(b'should not be less than 8 characters', response.data)
