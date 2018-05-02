from sqlalchemy.dialects.postgresql.base import UUID
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

import uuid

# from ..api import db
db.UUID = UUID

class Meal(db.Model):
    """This class represents the meals table.
    """

    __tablename__ = 'meals'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=lambda:uuid.uuid4().hex)
    title = db.Column(db.String(100))
    price = db.Column(db.Float)

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

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=lambda:uuid.uuid4().hex)
    date = db.Column(db.DateTime, index=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))


    def __init__(self, meal):
        """Initializes this class
        """
        self.meal_id = meal_id        
        
    @classmethod
    def set_menu(self):
        """Set menu and store it into the main database
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Menu: {}>".format(self.date)    

         