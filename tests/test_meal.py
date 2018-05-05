import unittest
import json
from api import db
from api.models import Meal
from tests.main import MainTestCase


class TestUserEndpoint(MainTestCase):
    
    def test_create_meal(self):
        """Testing meal creation"""
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef with chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)

    def test_get_all_meals(self):
        """Testing retrieval of all meals"""
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef mink chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)

            response = self.client.get('v2/api/meals')
            self.assertEqual(response.status_code, 200)

    def test_get_meal(self):
        """Test retrieve meal details
        """
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef mink chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)
        
            response = self.client.get('v2/api/meals/1')
            self.assertEqual(response.status_code, 200)

    def test_duplicate_attempts(self):
        """Testing attempt to create a duplicate meal
        """
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef mink chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef mink chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                b'You have already submitted a meal with the same title', response.data)

    def test_invalid_or_empty_data_input(self):
        """Testing attempt to create meal with invalid data"""
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef with Chicken'
            }))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Please fill in with valid data', response.data)

    def test_delete_meal(self):
        """Testing delete function
        """
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef mink chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)

            response = self.client.delete('v2/api/meals/1')
            self.assertEqual(response.status_code, 202)
            self.assertIn(b'Meal has been successfully deleted', response.data)

    def test_update_meal(self):
        """Testing meal update function
        """
        new_data = {
            'title': 'Chicken with Ugali',
            'price': '1000.00'
        }
        with self.client:
            response = self.client.post('v2/api/meals', data=json.dumps({
                'title': 'Beef mink chapati',
                'price': '600.00'
            }))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'Meal has been successfully created', response.data)
            response = self.client.put('v2/api/meals/1',
                                    data=json.dumps(new_data))
            self.assertEqual(response.status_code, 202)
            self.assertIn(b'The meal has been successfully updated', response.data)

if __name__ == '__main__':
    unittest.main()
