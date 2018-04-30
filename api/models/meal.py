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
        pass

    @classmethod
    def delete(cls, meal_id):
        """Deletes meal from the database
        """

        pass

    @classmethod
    def update(cls, meal_id, data):
        """Edits meal option
        """
        pass

    @classmethod
    def get_meals(cls):
        """Gets Meal Details
        """
        pass
            
    @classmethod
    def get_meal(cls, meal_id):
        """Gets Meal Details
        """
        pass               

    @classmethod
    def meal_already_exist(cls, meal_title):
        """Check if the meal to be added or updated already exists
        """
        pass   