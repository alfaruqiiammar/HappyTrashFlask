import json
import datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import ListTrashCategory
from flask_jwt_extended import jwt_required, get_jwt_claims
from apps import db, app, adminRequired

bp_trash_categories = Blueprint('trash_categories', __name__)
api = Api(bp_trash_categories)


class TrashCategoriesResource(Resource):
    """Class for storing HTTP request method for trash categories table"""

    def __init__(self):
        """Init function needed to indicate this is a class"""
        pass

    def options(self):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return {"status": "Ok"}, 200

    @adminRequired
    def post(self):
        """ Post a new trash category to trash_categories table

        Args: 
            category_name: A string of trash category name that admin has inputted 

        Returns:
            A dictionary contains the data that has been input to the table.
            For example:
            {
                "id": 1,
                "category_name": "plastik"
                "created_at": Sat, 26 Apr 2019 09:00:00 -0000
                "updated_at": Sat, 26 Apr 2019 09:00:00 -0000
            }
        """
        parser = reqparse.RequestParser()

        parser.add_argument('category_name', location='json', required=True)
        parser.add_argument('created_at', location='json')
        parser.add_argument('updated_at', location='json')

        args = parser.parse_args()

        trash_category = ListTrashCategory(args['category_name'])
        db.session.add(trash_category)
        db.session.commit()

        app.logger.debug('DEBUG : %s', trash_category)

        return marshal(trash_category, ListTrashCategory.response_fields), 200, {'Content_Type': 'application/json'}

    @jwt_required
    def get(self):
        """ Gets all trash category from trash_categories table

        Returns:
            An array of dictionaries consist of trash categories data.
            For example:
            [
                {
                    "id": 1,
                    "category_name": "plastik"
                    "created_at": Sat, 26 Apr 2019 09:00:00 -0000
                    "updated_at": Sat, 26 Apr 2019 09:00:00 -0000
                },
                {
                    "id": 2,
                    "category_name": "Kaca"
                    "created_at": Sat, 26 Apr 2019 09:01:00 -0000
                    "updated_at": Sat, 26 Apr 2019 09:02:00 -0000
                }    
            ]
        """
        categories = ListTrashCategory.query.order_by(
            ListTrashCategory.id.desc())

        trash_categories = []
        for category in categories:
            category = marshal(category, ListTrashCategory.response_fields)
            trash_categories.append(category)

        return trash_categories, 200, {'Content_Type': 'application/json'}

    @adminRequired
    def put(self, id):
        """ Edits category_name from a single record in trash_category table specified by id 

        Args:
            id: An integer of trash category's id
            category_name: A string of trash category's name(located in JSON)

        Returns:
            A dictionary that contains the updated data from the record edited. For example:
            {
                "id": 2,
                "category_name": "Kaca"
                "created_at": Sat, 26 Apr 2019 09:01:00 -0000
                "updated_at": Sat, 26 Apr 2019 22:00:00 -0000
            }

        Raise:
            Not Found(404): An error occured when the id inputted is not found in the table
            Bad Request(400): An error occured when the category_name inputted is null
        """
        parser = reqparse.RequestParser()

        parser.add_argument('category_name', location='json', required=True)

        args = parser.parse_args()
        category = ListTrashCategory.query.get(id)

        if category is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        if not args['category_name']:
            return {"Warning": "Name can not be null"}, 400, {'Content_Type': 'application/json'}

        category.category_name = args['category_name']
        category.updated_at = datetime.datetime.utcnow()

        db.session.commit()
        return marshal(category, ListTrashCategory.response_fields), 200, {'Content_Type': 'application/json'}

    @adminRequired
    def delete(self, id):
        """Delete a single record from trash categories table

        Args: 
            id: An integer of trash category's id which want to be deleted

        Returns:
            A dictionary of key 'status' which have value of sucess message

        Raise:
            Not Found(404): An error occured when the id inputted is not found in the table
        """
        category = ListTrashCategory.query.get(id)

        if category is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        db.session.delete(category)
        db.session.commit()
        return {"Status": "The data with id {} is deleted".format(id)}, 200, {'Content_Type': 'application/json'}


api.add_resource(TrashCategoriesResource, '', '/<id>')
