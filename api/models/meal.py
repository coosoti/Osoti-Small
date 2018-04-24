"""Meal Class to model meal object
"""

# from .models.database import Database


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
    def get_meal(cls, meal_id):
        """Gets Meal Details
        """
        pass 

