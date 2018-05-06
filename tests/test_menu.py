"""Testing the Menu Class
"""
import datetime
import uuid
from flask import json
from api.models.models import Meal
from tests.main import MainTestCase

sample_admin = {'username': 'victorvenosa',
                'email': 'osoticharles@gmail.com',
                'designation': 'caterer',
                'password': 'kulundeng',
                'confirm_password': 'kulundeng'
                }

login_admin = {
    'email': 'osoticharles@gmail.com',
    'password': 'kulundeng'
}

class MenuTests(MainTestCase):
    """Main Test
    """

    def test_set_up_menu(self):
        """Test set up today's menu 
        """
        with self.client:
            response = self.client.post(
                'api/v2/auth/register',
                data=json.dumps(sample_admin),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            response = self.client.post('api/v2/meals', data=json.dumps({
                'title': 'Beef with chapati',
                'price': '600.00'
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(login_admin),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            response = self.client.post('api/v2/menu', data=json.dumps({
                'selected_ids': ["1"]
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                b'Menu has been successfully created', response.data)

    
    def test_get_menu(self):
        """Test get today's menu 
        """
        with self.client:
            response = self.client.post(
                'api/v2/auth/register',
                data=json.dumps(sample_admin),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            response = self.client.post('api/v2/meals', data=json.dumps({
                'title': 'Beef with chapati',
                'price': '600.00'
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(login_admin),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            response = self.client.post('api/v2/menu', data=json.dumps({
                'selected_ids': ["1"]
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                b'Menu has been successfully created', response.data)
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(login_admin),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            response = self.client.get('api/v2/menu', headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 200)


    def test_set_up_menu_with_invalid_meal_id(self):
        """Test add meal to today's menu with invalid meal id 
        """
        with self.client:
            response = self.client.post(
                'api/v2/auth/register',
                data=json.dumps(sample_admin),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            response = self.client.post('api/v2/meals', data=json.dumps({
                'title': 'Beef with chapati',
                'price': '600.00'
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(login_admin),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            response = self.client.post('api/v2/menu', data=json.dumps({
                'selected_ids': ["a"]
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 400)


    def test_set_up_menu_with_non_existing_meal_id(self):
        """Test add meal to today's menu with a meal that is not in the meal options 
        """
        with self.client:
            response = self.client.post(
                'api/v2/auth/register',
                data=json.dumps(sample_admin),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            response = self.client.post('api/v2/meals', data=json.dumps({
                'title': 'Beef with chapati',
                'price': '600.00'
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(login_admin),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            response = self.client.post('api/v2/menu', data=json.dumps({
                'selected_ids': ['5']
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Meal selected not found', response.data)
