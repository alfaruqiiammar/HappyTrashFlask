# from flask import Blueprint
# from flask_restful import Resource, Api, reqparse, marshal, inputs
# from .model import Users
# from sqlalchemy import desc
# from apps import app, db
# from flask_jwt_extended import jwt_required, get_jwt_claims
import re

# bp_users = Blueprint('users', __name__)
# api = Api(bp_users)

def isEmailAddressValid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return False
    return True

def isMobilePhoneValid(mobile_phone):
    """Validate the mobile phone using a regex."""
    if not re.match("^0[0-9]{9,}$", mobile_phone):
        return False
    return True

tes1 = isEmailAddressValid('15@gm.com')
tes2 = isMobilePhoneValid('0811223993')
print(tes1)
print(tes2)

from passlib.hash import sha256_crypt

password = sha256_crypt.encrypt("password")
password2 = sha256_crypt.encrypt("password")

print(password)
print(password2)

print(sha256_crypt.verify("password", password2))
		

# class UsersResource(Resource):
#     """Class for storing HTTP request method for users table"""

#     def __init__(self):
#         """Init function needed to indicate this is a class, but never used"""
#         pass

#     def options(self, id):
#         """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
#         return {'Status': 'OK'}, 200

    

#     @jwt_required
#     def post(self):
#         """Post new data to users table and user attributes table

#         Retrieve data from user input located in JSON, validate the data, then post the data to users tables. 
        
        
#         All of the field is required, so it will be error if one of the field required is None. If the data is not valid,  

        
#         """
#         parser = reqparse.RequestParser()
#         parser.add_argument('client_key', location='json')
#         parser.add_argument('client_secret', location='json')
#         parser.add_argument('status', type=bool, location='json')
#         args = parser.parse_args()

#         # check_client_key = Clients.query.filter_by(client_key=args['client_key']).first()
#         check_client_key = Clients.is_exists(args['client_key'])
#         if check_client_key is True:
#             return {'status': 'Username already taken!'}, 500, {'Content-Type': 'application/json'}

#         client = Clients(args['client_key'], args['client_secret'], args['status'])
#         db.session.add(client)
#         db.session.commit()

#         app.logger.debug('DEBUG : %s', client)

#         return marshal(client, Clients.response_fields), 200, {'Content-Type': 'application/json'}

# api.add_resource(UsersResource, '')

