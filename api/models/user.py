"""User models
"""
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.database import Database

class User(Database):
    """User class
    """

    @classmethod
    def save(cls, data):
        """This method save user into the main store
        """
        data['password'] = generate_password_hash(data['password'])
        Database.register_user(data)

    @classmethod
    def user_already_exists(cls, email):
        """This method checks if user exists in the main store
        """
        for user in Database.users:
            if user['email']  == email:
                return True
        return False
    
    @classmethod
    def get_user(cls, email):
        """This method checks if the user exists and return the user detail
        """
        pass
    
    
    @classmethod
    def check_password(cls, user_id, raw_password):
        """This method is user raw password is similar to the hashed password
        """
        for user in Database.users:
            if user['id'] == user_id:
                if check_password_hash(user['password'], raw_password):
                    return True
        return False
        
        
    @classmethod
    def change_password(cls, user_id, password):
        """This method updates the user password
        """
        pass


    @classmethod
    def is_admin(cls, user_id, designation):
        """Check is the designation on the user is admin
        """ 
        # for user in Store.users:
        #   if user['designation'] == caterer:
        #       return True
        # return False
        pass