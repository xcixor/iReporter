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
        "dbname": 'ireporter',
        "user": 'developer',
        "password": 'developer',
        "host": 'localhost',
        "port": "5432"
    }


class Testing(Config):
    """Contains configurations for testing."""

    TESTING = True
    db = {
        "dbname": 'test_ireporter',
        "user": 'developer',
        "password": 'developer',
        "host": 'localhost',
        "port": "5432"
    }


class Production(Config):
    """Contains configurations for production setting."""

    DEBUG = False


# Register the configurations
config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
