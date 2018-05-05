import unittest

from api import db
from api.models import User
from tests.main import MainTestCase


class TestUser(MainTestCase):

    def test_encode_auth_token(self):
        sample_user = User(
            username='kulundeng',
            email='osoticharles@gmail.com',
            designation='caterer',
            password='password1'
        )
        db.session.add(sample_user)
        db.session.commit()
        auth_token = sample_user.encode_auth_token(sample_user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        sample_user = User(
            username='kulundeng',
            email='osoticharles@gmail.com',
            designation='caterer',
            password='password1'

        )
        db.session.add(sample_user)
        db.session.commit()
        auth_token = sample_user.encode_auth_token(sample_user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == 1)    

if __name__ == '__main__':
    unittest.main()