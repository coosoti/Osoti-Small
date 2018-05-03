from flask_testing import TestCase

from api import app, db
from instance.config import app_config


class MainTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(app_config['testing'])
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()