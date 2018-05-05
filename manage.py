# manage.py


import os
import unittest
import coverage
from flasgger import Swagger

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'api/tests/*',
        'instance/config.py',
        'api/*/__init__.py'
    ]
)
COV.start()

from api import app, db, models

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()

SWAGGER_CONFIG = {
    "headers": [],
    "title": "Book-A-Meal",
    "specs": [
        {
            "version": "1.0",
            "title": "API Version 1",
            "endpoint": 'apispecs',
            # "route": '/api/v1/docs.json',
             "route": '/api/v2/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda rule: True,
        }
    ],
    "static_url_path": "/swagger_files",
    "swagger_ui": True,
    "specs_route": "/docs"
    # "specs_route": "/api/v2"
}
TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Book-A-Meal",
        "description": "Book-A-Meal API version 1.0",
        "version": "1.0"
    },
    "consumes": [
        "application/json",
    ],
    "produces": [
        "application/json",
    ],
    "schemes": [
        "http",
        "https"
    ],
    "operationId": "getmyData"
}


SWAGGER = Swagger(app, config=SWAGGER_CONFIG, template=TEMPLATE) 

if __name__ == '__main__':
    manager.run()