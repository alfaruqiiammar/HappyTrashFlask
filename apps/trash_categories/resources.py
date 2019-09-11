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

    def __init__(self):
        pass

    def options(self):
        return {"status": "Ok"}, 200

    #@adminRequired
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('category_name', location='json', required=True)
        parser.add_argument('created_at', location='json')
        parser.add_argument('updated_at', location='json')

        args = parser.parse_args()

        new_trash_category = {
            'category_name': args['category_name'],
            'created_at' : args['created_at'],
            'updated_at' : args['updated_at']
        }

        trash_category = ListTrashCategory(new_trash_category)
        db.session.add(trash_category)
        db.session.commit()

        app.logger.debug('DEBUG : %s', trash_category)

        return marshal(trash_category, ListTrashCategory.response_fields), 200, {'Content_Type': 'application/json'}

    def get(self):
        categories = ListTrashCategory.query

        trash_categories = []
        for category in categories:
            category = marshal(category, ListTrashCategory.response_fields)
            trash_categories.append(category)
        
        return trash_categories, 200, {'Content_Type' : 'application/json'}

    def put(self, id):
        parser = reqparse.RequestParser()

        parser.add_argument('category_name', location = 'json', required = True)

        args = parser.parse_args()
        category = ListTrashCategory.query.get(id)

        if category is None:
            return {'status' : 'Not Found'}, 404, {'Content_Type' : 'application/json'}
        
        category.category_name = args['category_name']
        category.updated_at = datetime.datetime.utcnow()
        return marshal(category, ListTrashCategory.response_fields), 200, {'Content_Type' : 'application/json'}
        

    def delete(self, id):
        category = ListTrashCategory.query.get(id)

        if category is None:
            return {'status' : 'Not Found'}, 404, {'Content_Type' : 'application/json'}
        
        db.session.delete(category)
        


api.add_resource(TrashCategoriesResource, '', '/<id>')
