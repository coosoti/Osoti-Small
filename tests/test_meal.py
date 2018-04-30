"""Testing the Meal Class
"""
import uuid
import datetime
from flask import json
from tests.test_api import MainTests
from api.models.meal import Meal
from api.models.database import Database 

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

    # testing menu routes
    def test_set_up_menu(self):
        """Test add meal to today's menu list 
        """
        response = self.app.post('/api/v1/menu', data=json.dumps({
            'date': datetime.datetime.today().strftime('%Y-%m-%d'),
            'meal': self.meal_data
            }))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Menu Successfully Created', response.data)

    def test_get_menu(self):
        """Testing retrieval of menu
        """
        response = self.app.get('/api/v1/menu')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'6 meals found in today menu', response.data)

    def  test_order_meal(self):
        """Test order meal from today's menu
        """
        response = self.app.post('/api/v1/orders', data=json.dumps({
            'id': uuid.uuid4().hex,
            'orders_data': self.meal_data
            }))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'You have successfully ordered a meal', response.data)         
    
    def test_update_order(self):
        """Testing meal update function
        """
        new_menu_meal = {
            'title': 'Chicken with Ugali',
            'price': '1000.00'
        }
        Database.orders.append(self.orders_data)
        response = self.app.put('/api/v1/menu/' + self.orders_data['id'],
            data=json.dumps(new_menu_meal))
        self.assertEqual(response.status_code, 202)
        self.assertIn(b'The order has been successfully updated', response.data)

    
    def test_get_all_orders(self):
        """Testing retrieval of all meals
        """
        response = self.app.get('/api/v1/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'There are 5 orders', response.data)    
        




