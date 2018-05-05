import unittest
import json
from api import db
from api.models.models import User
from tests.main import MainTestCase


class TestUserEndpoint(MainTestCase):
    
    def test_registration(self):
        """ Test for user signup 
        """
        with self.client:
            response = self.client.post('api/v2/auth/register',
                data=json.dumps(dict(
                    username='kulundeng',
                    email='vicharles@gmail.com',
                    designation='caterer',
                    password='password1',
                    confirm_password='password1'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'You are successfully registered.')
            self.assertEqual(response.status_code, 201)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            response = self.client.post(
                'api/v2/auth/register',
                data=json.dumps(dict(
                    username='victorvenosa',
                    email='osoticharles@gmail.com',
                    designation='customer',
                    password='kulundeng',
                    confirm_password='kulundeng'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(
                data['message'] == 'You are successfully registered.'
            )
            self.assertEqual(response.status_code, 201)
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(dict(
                    email='osoticharles@gmail.com',
                    password='kulundeng'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'You have successfully logged in')
            self.assertEqual(response.status_code, 200)    

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(dict(
                    email='victorvenosa@gmail.com',
                    password='thatisthewayitis'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertEqual(response.status_code, 404)        

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            response = self.client.post(
                'api/v2/auth/register',
                data=json.dumps(dict(
                    username='victorvenosa',
                    email='osoticharles@gmail.com',
                    designation='customer',
                    password='kulundeng',
                    confirm_password='kulundeng'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(
                data['message'] == 'You are successfully registered.')
            self.assertEqual(response.status_code, 201)
            # user login
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(dict(
                    email='osoticharles@gmail.com',
                    password='kulundeng'
                )),
                content_type='application/json'
            )
            data= json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'You have successfully logged in')
            self.assertEqual(response.status_code, 200)
            # valid token logout
            response = self.client.post(
                'api/v2/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            # self.assertTrue(data['message'] == 'You have successfully logged out')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()




