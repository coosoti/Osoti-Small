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
         