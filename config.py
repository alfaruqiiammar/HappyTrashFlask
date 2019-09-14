from dotenv import load_dotenv
import os

load_dotenv()

# db_user = os.environ.get('DB_USER')
# db_password = os.environ.get('DB_PASSWORD')

db_user = ${DB_USER}
db_password = ${DB_PASSWORD}

# db_user = 'HappyTrash'
# db_password = 'HappyTerus'

class Config():
    pass

class DevelopmentConfig(Config):
    """Class for storing information about development database

    Attributes:
        DEBUG: a boolean indicates the debug mode is activated or not
        SQLALCHEMI_DATABASE_URI: a string that contain information about uri to access development database
    """
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@127.0.0.1:3306/happy_trash'.format(db_user, db_password)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@happytrash.chrpcgbaee9q.ap-southeast-1.rds.amazonaws.com:3306/happy_trash'.format(db_user, db_password)

class TestingConfig(Config):
    """Class for storing information about testing database

    Attributes:
        TESTING: a boolean indicates the testing mode is activated or not
        SQLALCHEMI_DATABASE_URI: a string that contain information about uri to access testing database
    """
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@127.0.0.1:3306/happy_trash_testing'.format(db_user, db_password)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@happytrash.chrpcgbaee9q.ap-southeast-1.rds.amazonaws.com:3306/happy_trash_testing'.format(db_user, db_password)