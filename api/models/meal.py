"""Meal Class to model meal object
"""

from api.models.database import Database


class Meal(object):
    """Meal Model
    """

    def __init__(self):
        """Initializes class
        """
        pass

    @classmethod
    def save(cls, data):
        """Saves meal option to the meals database
        """
        Database.save_meal(data)

    @classmethod
    def delete(cls, meal_id):
        """Deletes meal from the database
        """
        Database.delete_meal(meal_id)

    @classmethod
    def update(cls, meal_id, data):
        """Edits meal option
        """
        Database.update_meal(meal_id, data)

    @classmethod
    def get_meals(cls):
        """Gets Meal Details
        """
        meals = [meal for meal in Database.meals]
        return meals
            
    @classmethod
    def get_meal(cls, meal_id):
        """Gets Meal Details
        """
        for meal in Database.meals:
            if meal['id'] == meal_id:
                return meal               

    @classmethod
    def meal_already_exist(cls, meal_title):
        """Check if the meal to be added or updated already exists
        """
        for meal in Database.meals:
            if (meal['title'].lower() == meal_title.lower()):
                return True
        return False        

