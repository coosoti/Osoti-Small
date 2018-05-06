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
    """Main Test"""

    def test_make_an_order(self):
        """Test make an order"""
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
                'selected_ids': ["1"]
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
            response = self.client.post('api/v2/orders', data=json.dumps({
                'selected_meal_id': "1"
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                b'You order is successfull', response.data)
    
    def test_get_all_orders(self):
        """Testing retrieval of all orders
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
                'selected_ids': ["1"]
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
            response = self.client.post('api/v2/orders', data=json.dumps({
                'selected_meal_id': "1"
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                b'You order is successfull', response.data)
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(login_admin),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            response = self.client.get('api/v2/orders', headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 200)

    def test_get_one_order(self):
        """Testing get one order
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
                'selected_ids': ["1"]
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
            response = self.client.post('api/v2/orders', data=json.dumps({
                'selected_meal_id': "1"
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                b'You order is successfull', response.data)
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(login_admin),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            response = self.client.get('api/v2/orders/1', headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 200)

    def test_update_one_order(self):
        """Testing get one order
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
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(login_admin),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            response = self.client.post('api/v2/meals', data=json.dumps({
                'title': 'Water with chapati',
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
                'selected_ids': ["1"]
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
            response = self.client.post('api/v2/orders', data=json.dumps({
                'selected_meal_id': "1"
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                b'You order is successfull', response.data)
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(login_admin),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            response = self.client.put('api/v2/orders/1', data=json.dumps({
                'selected_meal_id': ["2"]
            }), headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response.data.decode()
                    )['auth_token']
                ))
            self.assertEqual(response.status_code, 200)
