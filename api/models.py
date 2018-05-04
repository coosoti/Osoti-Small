from sqlalchemy.dialects.postgresql.base import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
import datetime

from api import app, db, bcrypt
# db = SQLAlchemy()


menu_meals = db.Table('menu_meals',
    db.Column('menu_id', db.Integer, db.ForeignKey('menus.id')),
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'))
)


class Meal(db.Model):
    """This class represents the meals table.
    """

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Float)
    # menu_meals = db.relationship('Menu', secondary=menu_meals,
    #     backref=db.backref('meals', lazy='dynamic', uselist=True))

    def __init__(self, title, price):
        """initialize with title and price.
        """
        self.title = title
        self.price = price 


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def meal_already_exist(cls, title):
        """Check if the meal to be added or updated already exists
        """
        meal = Meal.query.filter_by(title = title).first()
        if meal:
            return True
        return False    

    @staticmethod
    def get_all():
        return Meal.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Meal: {}>".format(self.title)


class Menu(db.Model):
    """Menu model
    """

    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    menu_meals = db.relationship('Meal', secondary=menu_meals,
        backref=db.backref('meals', lazy=True, uselist=True))

    def __init__(self, date):
        """Initializes this class
        """
        self.date = date        
        
    @classmethod
    def set_menu(self):
        """Set menu and store it into the main database
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Menu: {}>".format(self.menu_meals) 


class User(db.Model):
    """ User Model for storing user related details 
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    designation = db.Column(db.String(32), nullable=False)

    def __init__(self, username, email, password, designation):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.designation = designation

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False           

         