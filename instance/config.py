"""Contains configurations for the app."""

import os


class Config:
    """Contains the basic settings for all configurations."""

    debug = False
    SECRET_KEY = os.urandom(30)

    @staticmethod
    def init_app(app):
        """To perform configuration specific initializations."""
        pass


class Development(Config):
    """Contains configurations to be used by developer."""

    DEBUG = True
    db = {
        "dbname": os.getenv('dbname'),
        "user": os.getenv('user'),
        "password": os.getenv('password'),
        "host": os.getenv('host'),
        "port": os.getenv('port')
    }


class Testing(Config):
    """Contains configurations for testing."""

    TESTING = True
    db = {
        "dbname": os.getenv('test_dbname'),
        "user": os.getenv('user'),
        "password": os.getenv('password'),
        "host": os.getenv('host'),
        "port": os.getenv('port')
    }


class Production(Config):
    """Contains configurations for production setting."""

    DEBUG = False


# Register the configurations
CONFIG = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
