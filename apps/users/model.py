from apps import db
from flask_restful import fields

class Users(db.Model):
    """Class for storing information about users table

    Attributes:
        __tablename__: a string of table name
        id: an integer of user's id
        name: a string of user's name
        email: a string of user's email
        mobile_phone: a string of user's mobile_phone
        password: a string of user's password
        role: a boolean that indicates user role. True for admin and False for user
        date_created: a datetime that indicates when the account created
        date_updated: a datetime that indicates when the account last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    mobile_phone = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Boolean, nullable=False)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'mobile_phone': fields.String,
        'role': fields.Boolean
    }

    def __init__(self, name, email, mobile_phone, password, role):
        """Inits Users with data that user inputted

        The data already validated on the resources function

        Args:
            self.name: a string of user's name
            self.email: a string of user's email
            self.mobile_phone: a string of user's mobile_phone
            self.password: a string of user's password
            self.role: a boolean that indicates user role. True for admin and False for user
        """
        self.name = name
        self.email = email
        self.mobile_phone = mobile_phone
        self.password = password
        self.role = role