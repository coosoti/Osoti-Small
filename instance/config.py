import os


class Config(object):
    """Parent configuration class.
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    basedir = os.path.abspath(os.path.dirname(__file__))
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI ="postgresql://postgres:28201903@localhost:5432/bam"

class DevelopmentConfig(Config):
    """Configurations for Development.
    """
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing.
    """
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging.
    """
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production.
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
