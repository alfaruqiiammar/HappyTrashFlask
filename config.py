import os

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

class Config():
    pass

class DevelopmentConfig(Config):
    """Class for storing information about development database

    Attributes:
        DEBUG: a boolean indicates the debug mode is activated or not
        SQLALCHEMI_DATABASE_URI: a string that contain information about uri to access development database
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@127.0.0.1:3306/happy_trash"

class TestingConfig(Config):
    """Class for storing information about testing database

    Attributes:
        TESTING: a boolean indicates the testing mode is activated or not
        SQLALCHEMI_DATABASE_URI: a string that contain information about uri to access testing database
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@127.0.0.1:3306/happy_trash_testing"