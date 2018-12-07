"""Contains configurations for the app."""

import os


class Config:
    """Contains the basic settings for all configurations."""

    PROPAGATE_EXCEPTIONS = True


class Development(Config):
    """Contains configurations to be used by developer."""

    DEBUG = True


class Testing(Config):
    """Contains configurations for testing."""

    TESTING = True


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
