"""Order Class
"""
from api.models.database import Database

class Order():
    """Order model
    """

    def __init__(self):
        """Initializes this class
        """
        pass    
        
    @classmethod
    def add_order(cls, data):
        """add order store it into the main database
        """
        Database.save_order(data)

    @classmethod
    def update(cls, order_id, data):
        """Edits order option
        """
        Database.update_orders(order_id, data) 

    @classmethod
    def get_order(cls, order_id):
        """Gets Order Details
        """
        for order in Database.orders:
            if order['id'] == order_id:
                return order     