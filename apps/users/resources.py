from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Users
from apps.user_attributes.model import UserAttributes
from sqlalchemy import desc
from apps import app, db, adminRequired, userRequired
from flask_jwt_extended import jwt_required, get_jwt_claims
from passlib.hash import sha256_crypt

bp_users = Blueprint('users', __name__)
api = Api(bp_users)


class UsersResource(Resource):
    """Class for storing HTTP request method for users table"""

    def __init__(self):
        """Init function needed to indicate this is a class, but never used"""
        pass

    def options(self, id=None):
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

        users = Users(args['name'], args['email'],
                      args['mobile_number'], args['password'], False)
        if not users.isEmailAddressValid(args['email']):
            return {'message': 'Invalid email format!'}, 400, {'Content-Type': 'application/json'}

        # We use isMobileNumberValid function to check whether mobile number inputted is valid or not

        if not users.isMobileNumberValid(args['mobile_number']):
            return {'message': 'Invalid mobile number format!'}, 400, {'Content-Type': 'application/json'}

        # Check whether email is already exist in database

        check_email = users.isEmailExist(args['email'])
        if check_email is True:
            return {'message': 'Email already listed!'}, 400, {'Content-Type': 'application/json'}

        # Check whether mobile_number is already exist in database

        check_mobile_number = users.isMobileNumberExist(args['mobile_number'])
        if check_mobile_number is True:
            return {'message': 'Mobile number already listed!'}, 400, {'Content-Type': 'application/json'}

        # Encrypt password using sha256

        password_encrypted = sha256_crypt.hash(args['password'])

        # Input data to users table

        user = Users(args['name'], args['email'],
                     args['mobile_number'], password_encrypted, False)
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

    @userRequired
    def get(self, id):
        """Get a user's detail by id. A user can not access another user's data

        Raise :
            403 : Occured when user try to access another user's data
            404 : Occured when the data is not found in the table
        """

        user = get_jwt_claims()
        user_requested = Users.query.get(id)
        user_req_attr = UserAttributes.query.filter_by(user_id=id).first()
        if user_requested is None:
            return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}

        requested = marshal(user_requested, Users.response_fields)
        attr_requested = marshal(user_req_attr, UserAttributes.response_fields)
        attr_requested.pop('user_id')

        if user['id'] != requested['id']:
            return {'Warning': 'You are not allowed to access others credentials'}, 403, {'Content-Type': 'application/json'}

        result = requested.update(attr_requested)

        return requested, 200, {'Content-Type': 'application/json'}

    @userRequired
    def put(self):
        """edit user credentials"""

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('mobile_number', location='json')
        parser.add_argument('password', location='json')
        args = parser.parse_args()

        claims = get_jwt_claims()
        user_edited = Users.query.get(claims['id'])

        users = Users("dummy", "dummy", "dummy", "dummy", False)

        # Cheks if user input a name

        if args['name'] is not None:
            user_edited.name = args['name']

        # checks email and edit it

        if args['email'] is not None:

            if not users.isEmailAddressValid(args['email']):
                return {'message': 'Invalid email format!'}, 400, {'Content-Type': 'application/json'}

            check_email = users.isEmailExist(args['email'])
            if check_email is True:
                return {'message': 'Email already listed!'}, 400, {'Content-Type': 'application/json'}

            user_edited.email = args['email']

        # checks the number phone and edit it

        if args['mobile_number'] is not None:

            if not users.isMobileNumberValid(args['mobile_number']):
                return {'message': 'Invalid mobile number format!'}, 400, {'Content-Type': 'application/json'}

            check_mobile_number = users.isMobileNumberExist(
                args['mobile_number'])
            if check_mobile_number is True:
                return {'message': 'Mobile number already listed!'}, 400, {'Content-Type': 'application/json'}

            user_edited.mobile_number = args['mobile_number']

        # checks if user input a new password

        if args['password'] is not None:
            password_encrypted = sha256_crypt.hash(args['password'])
            user_edited.password = password_encrypted

        db.session.commit()

        return marshal(user_edited, Users.response_fields), 200, {'Content-Type': 'application/json'}


class UsersForAdminResource(Resource):

    def __init__(self):
        pass

    def options(self, id=None):
        return {'Status': 'OK'}, 200

    @adminRequired
    def get(self, id):
        """get user's data  by id

        Returns : A dict contains all profile data from a specific user. Example :
        {
            "id" : 1,
            "name" : "user",
            "email" : "exp@exp.com"
            "mobile_number" : "0898787878"
        }
        """
        # find user's data in table

        user = Users.query.get(id)

        if user is None:
            return {'Status': 'Not Found'}, 404
        user_dict = marshal(user, Users.response_fields)

        # return the data

        return user_dict, 200, {'Content-Type': 'application/json'}


class AllUserResource(Resource):

    def __init__(self):
        pass

    def options(self, id=None):
        return {'Status': 'OK'}, 200

    @adminRequired
    def get(self):
        """get all user's data

            Returns : An array of dictionary contains all data from users. Example :
            [
                {
                    "id" : 1,
                    "name" : "user",
                    "email" : "exp@exp.com"
                    "mobile_number" : "0898787878"
                },
                {
                    "id" : 2,
                    "name" : "user2",
                    "email" : "exp2@exp.com"
                    "mobile_number" : "08298787878"
                }
            ]
        """
        users = Users.query
        result = []
        for user in users:
            user = marshal(user, Users.response_fields)
            attr = UserAttributes.query.filter_by(user_id=user['id'])
            attr = marshal(attr, UserAttributes.response_fields)
            attr.pop('user_id')
            data = user.update(attr)
            result.append(user)

        return result, 200, {'Content-Type': 'application/json'}


api.add_resource(UsersResource, '', '/<id>')
api.add_resource(UsersForAdminResource, '/admin', '/admin/<id>')
api.add_resource(AllUserResource, '/all')
