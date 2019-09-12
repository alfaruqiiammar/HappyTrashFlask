from apps import db
from flask_restful import fields
import re

class Users(db.Model):
    """Class for storing information about users table

    Attributes:
        __tablename__: a string of table name
        id: an integer of user's id
        name: a string of user's name
        email: a string of user's email
        mobile_number: a string of user's mobile_number
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
    mobile_number = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Boolean, nullable=False)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'mobile_number': fields.String,
        'role': fields.Boolean
    }

    login_response_field = {
        'id': fields.Integer,
        'email': fields.String,
        'password': fields.String,
    }

    def __init__(self, name, email, mobile_number, password, role):
        """Inits Users with data that user inputted

        The data already validated on the resources function

        Args:
            name: a string of user's name
            email: a string of user's email
            mobile_number: a string of user's mobile_number
            password: a string of user's password
            role: a boolean that indicates user role. True for admin and False for user
        """
        self.name = name
        self.email = email
        self.mobile_number = mobile_number
        self.password = password
        self.role = role

    def isEmailAddressValid(email):
        """Validate the email address using a regex."""
        if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return False
        return True

    def isMobileNumberValid(mobile_number):
        """Validate the mobile phone using a regex."""
        if not re.match("^0[0-9]{9,}$", mobile_number):
            return False
        return True	

    @classmethod
    def isEmailExist(cls, email):
        """Check whether email already listed in database"""
        all_data = cls.query.all()


        # Make a list of email listed in database

        existing_email = [item.email for item in all_data]


        if email in existing_email:
            return True

        return False

    @classmethod
    def isMobileNumberExist(cls, mobile_number):
        """Check whether mobile number already listed in database"""
        all_data = cls.query.all()


        # Make a list of email listed in database

        existing_mobile_number = [item.mobile_number for item in all_data]
        

        if mobile_number in existing_mobile_number:
            return True

        return False