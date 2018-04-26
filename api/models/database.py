"""Database class to store data - implemented by data structures
"""

class Database(object):
    """Main db to store all data
    """

    meals = []
    menu = {}
    orders = []
    users = []
    jwt_tokens = []

    def __init__(self):
        """Initializes the class Database
        """
        pass

    @classmethod
    def save_token(cls, token):
        """Method to save generated token"""
        cls.jwt_tokens.append(token)

    @classmethod
    def remove_token(cls, token):
        """Method for removing auth token"""
        cls.jwt_tokens.remove(token)

    @classmethod
    def register_user(cls, data):
        """Method for saving user"""
        cls.users.append(data)

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
        cls.meals[:] = [meal for meal in cls.meals if meal.get('id') !=meal_id]

    @classmethod
    def update_meal(cls, meal_id, data):
        """This method will edit a meal option
        """
        for key in range(0, len(cls.meals)):
            if cls.meals[key]['id'] == meal_id:
                # this appends existing meal id to the data
                data['id'] = meal_id
                cls.meals[key] = data
                break          
           
    # Methods for menu
    @classmethod
    def save_menu(cls, meal_id):
        """This method appends meal to the menu list
        """

        pass

    # Methods for orders
    @classmethod
    def save_order(cls, data):
        """This method saves user's order to the orders stores
        """
        cls.orders.append(data)

    @classmethod
    def update_order(cls, order_id):
        """This method will edit user's order from the orders list
        """

        pass

    @classmethod
    def set_menu(cls, date, data):
        """Set menu method
        """        
        if not date in cls.menu:
            cls.menu[date] = []
        cls.menu[date].append(data)


              
                
