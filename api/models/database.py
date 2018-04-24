"""Database class to store data - implemented by data structures
"""

class Database(object):
    """Main db to store all data
    """

    meals = []
    menu = []
    orders = []
    users = []

    def __init__(self):
        """Initializes the class Database
        """
        pass

    # Methods for meals
    @classmethod
    def save_meal(cls, data):
        """This method will append meal option to the meal's list
        """
        cls.meals.append(data)        

    @classmethod
    def delete_meal(cls, meal_id):
        """This method will remove meal option from the meal's list
        """

        pass

    @classmethod
    def update_meal(cls, meal_id, data):
        """This method will edit a meal option
        """

        pass          

    # Methods for menu
    @classmethod
    def save_menu(cls, meal_id):
        """This method appends meal to the menu list
        """

        pass

    # Methods for orders
    @classmethod
    def save_order(cls, meal_id):
        """This method saves user's order to the orders stores
        """
        pass

    @classmethod
    def update_order(cls, order_id):
        """This method will edit user's order from the orders list
        """

        pass    
                
