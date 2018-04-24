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
<<<<<<< HEAD
        Database.save_meal(data)
=======
        pass
>>>>>>> 157011695-chore/project-set-up

    @classmethod
    def delete(cls, meal_id):
        """Deletes meal from the database
        """

        pass

    @classmethod
    def update(cls, meal_id, data):
        """Edits meal option
        """
<<<<<<< HEAD
        Database.update_meal(meal_id, data)
=======
        pass
>>>>>>> 157011695-chore/project-set-up

    @classmethod
    def get_meals(cls):
        """Gets Meal Details
        """
<<<<<<< HEAD
        meals = [meal for meal in Database.meals]
        return meals
=======
        pass
>>>>>>> 157011695-chore/project-set-up
            
    @classmethod
    def get_meal(cls, meal_id):
        """Gets Meal Details
        """
<<<<<<< HEAD
        for meal in Database.meals:
            if meal['id'] == meal_id:
                return meal               
=======
        pass               
>>>>>>> 157011695-chore/project-set-up

    @classmethod
    def meal_already_exist(cls, meal_title):
        """Check if the meal to be added or updated already exists
        """
<<<<<<< HEAD
        for meal in Database.meals:
            if (meal['title'].lower() == meal_title.lower()):
                return True
        return False        


=======
        pass   
>>>>>>> 157011695-chore/project-set-up
