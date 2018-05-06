import unittest
import os 
from flask import current_app
from flask_testing import TestCase
from instance.config import app_config

from api import app

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object(app_config['development'])
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL')
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object(app_config['testing'])
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://postgres:28201903@localhost:5432/test'
        )

def test_app_is_development(self):
    self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
    self.assertTrue(app.config['DEBUG'] is True)
    self.assertFalse(current_app is None)
    self.assertTrue(
        app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://postgres:@localhost/flask_jwt_auth'
    )
