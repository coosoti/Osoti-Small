"""User models
"""
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.database import Database


class User(Database):
    """User class
    """

    def __init__(self):
        """Initializer for this class
        """
        pass

    @classmethod
    def save(cls, data):
        """This method save user into the main database
        """
        data['password'] = generate_password_hash(data['password'])
        Database.register_user(data)

    @classmethod
    def user_already_exists(cls, email):
        """This method checks if user exists in the main database
        """
        for user in Database.users:
            if user['email'] == email:
                return True
        return False

    @classmethod
    def get_user(cls, email):
        """This method checks if the user exists and return the user detail
        """
        for user in Database.users:
            if user['email'] == email:
                return user
        return False

    @classmethod
    def add_token(cls, token):
        """This method save auth token to the main database"""
        Database.save_token(token)

    @classmethod
    def token_exists(cls, user_token):
        """This method checks if the auth token exists in the main database"""
        for token in Database.jwt_tokens:
            if token == user_token:
                return True
        return False

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
    def is_admin(cls, designation):
        """Check is the designation on the user is admin
        """
        for user in Database.users:
            if user['designation'].lower() == "caterer":
                return True
        return False

    @classmethod
    def get_user_designation(cls, designation):
        """Check is the designation on the user is admin
        """
        for user in Database.users:
            if user['designation'] == designation:
                return user
        return False
