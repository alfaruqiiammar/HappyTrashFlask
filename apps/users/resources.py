from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Users
from apps.user_attributes.model import UserAttributes
from sqlalchemy import desc
from apps import app, db
from flask_jwt_extended import jwt_required, get_jwt_claims
from passlib.hash import sha256_crypt

bp_users = Blueprint('users', __name__)
api = Api(bp_users)

class UsersResource(Resource):
    """Class for storing HTTP request method for users table"""

    def __init__(self):
        """Init function needed to indicate this is a class, but never used"""
        pass

    def options(self):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return {'Status': 'OK'}, 200	

    def post(self):
        """Post new data to users table and user attributes table

        Retrieve data from user input located in JSON, validate the data, then post the data to users tables.

        Args (located in JSON):
            name: A string of user's name
            email: A string of user's email
            mobile_number: A string of user's mobile_number
            password: A string of user's password

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "name": "user",
                "email": "user@mail.com",
                "mobile_number": "08111111111",
            }
        
        Raises: 
            Bad Request (400): An error that occured when some of the field is missing, or if the data is not valid (email and mobile phone inputted is wrong formatted)        
        """

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('mobile_number', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        # We use isEmailAddressValid function to check whether email inputted is valid or not

        if not Users.isEmailAddressValid(args['email']):
            return { 'message': 'Invalid email format!'}, 400, {'Content-Type': 'application/json'}


        # We use isMobileNumberValid function to check whether mobile number inputted is valid or not

        if not Users.isMobileNumberValid(args['mobile_number']):
            return { 'message': 'Invalid mobile number format!'}, 400, {'Content-Type': 'application/json'}


        # Check whether email is already exist in database

        check_email = Users.isEmailExist(args['email'])
        if check_email is True:
            return {'message': 'Email already listed!'}, 400, {'Content-Type': 'application/json'}


        # Check whether mobile_number is already exist in database

        check_mobile_number = Users.isMobileNumberExist(args['mobile_number'])
        if check_mobile_number is True:
            return {'message': 'Mobile number already listed!'}, 400, {'Content-Type': 'application/json'}


        # Encrypt password using sha256

        password_encrypted = sha256_crypt.encrypt(args['password'])

        # Input data to users table

        user = Users(args['name'], args['email'], args['mobile_number'], password_encrypted, False)
        db.session.add(user)
        db.session.commit()


        # get user id
        
        user_contain = marshal(user, Users.response_fields)
        user_id = user_contain['id']


        # Input data to user attributes table

        user_attributes = UserAttributes(user_id, 0, 0, False)
        db.session.add(user_attributes)
        db.session.commit()


        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}

api.add_resource(UsersResource, '')

