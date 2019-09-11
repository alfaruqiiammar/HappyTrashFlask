import os

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

print(db_user)
print(db_password)

class Config():
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@127.0.0.1:3306/e_commerce_project'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@127.0.0.1:3306/e_commerce_project_testing'