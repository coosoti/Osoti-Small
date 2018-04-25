"""Testing the Meal Class
"""

from flask import json
from tests.test_api import MainTests
from api.models.meal import Meal

class MealTests(MainTests):
    """Main Test
    """

    def test_create_meal(self):
        """Testing meal creation
        """
        response = self.app.post('/api/v1/meals', data=json.dumps({
            'title': 'Beef with chapati',
            'price': '600.00'
            }))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Meal Successfully Created', response.data)

    def test_get_all_meals(self):
        """Testing retrieval of all meals
        """
        response = self.app.get('/api/v1/meals')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'There are 6 meals', response.data)

    def test_get_meal(self):
        """Test retrieve meal details
        """
        response = self.app.get('/api/v1/meals/' + self.meal_data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'meal found', response.data)


    def test_duplicate_attempts(self):
        """Testing attempt to create a duplicate meal
        """
        Meal().save(self.meal_data)
        response = self.app.post('/api/v1/meals', 
            data=self.meal_data,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'This meal option has been registered', response.data)    

    def test_duplicate_attempts(self):
        """Testing attempt to create a duplicate meal
        """

        data = self.meal_data
        Meal().save(self.meal_data)
        response = self.app.post('/api/v1/meals', 
            data=self.meal_data,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'This meal option has been registered', response.data)

    def test_invalid_or_empty_data_input(self):
        """Testing attempt to create meal with invalid data
        """

        response= self.app.post('/api/v1/meals', data=json.dumps({
            'title': 'Beef with Chicken',
            }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please required data', response.data)

    def test_delete_meal(self):
        """Testing delete function
        """
        Meal.save(self.meal_data)
        response = self.app.delete('/api/v1/meals/' + self.meal_data['id'],
            data={})
        self.assertEqual(response.status_code, 202)
        self.assertIn(b'Meal has been successfully deleted', response.data)

    def test_update_meal(self):
        """Testing meal update function
        """
        new_data = {
            'title': 'Chicken with Ugali',
            'price': '1000.00'
        }
        Meal.save(self.meal_data)
        response = self.app.put('/api/v1/meals/' + self.meal_data['id'],
            data=json.dumps(new_data))
        self.assertEqual(response.status_code, 202)
        self.assertIn(b'The meal has been successfully updated', response.data)

                         


