from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import UserAttributes
from sqlalchemy import desc
from apps import app, db, userRequired
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_user_attributes = Blueprint('user_attributes', __name__)
api = Api(bp_user_attributes)


class UserAttributesResource(Resource):
    """class for storing HTTP request used to update onboarding status in user_attributes table"""

    def __init__(self):
        """Init function needed to indicate this is a class"""
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return {'Status': 'Ok'}, 200

    @userRequired
    def put(self):
        """Change user's on boarding status from True to False,vice versa

        Args (retrieved from jwt claims):
            claims: a dict consist of user's information

        Returns:
            A dictionary mapping keys to corresponding value. For example:
                {
                    "id":5,
                    "user_id":5,
                    "point": 10,
                    "total_trash": 100,
                    "onboarding_status": True
                }
        """
        claims = get_jwt_claims()
        user_attr = UserAttributes.query.filter_by(
            user_id=claims['id']).first()

        new_onboard_status = not user_attr.onboarding_status
        user_attr.onboarding_status = new_onboard_status
        db.session.commit()

        return marshal(user_attr, UserAttributes.response_fields), 200


api.add_resource(UserAttributesResource, '')
