import json
import datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import ListTrash
from flask_jwt_extended import jwt_required, get_jwt_claims
from apps import db, app, adminRequired

bp_trashes = Blueprint('trashes', __name__)
api = Api(bp_trashes)


class TrashResource(Resource):

    def __init__(self):
        pass

    def options(self, id=None):
        return {"status": "Ok"}, 200

    @adminRequired
    def post(self):
        """ Post a new trash to trashes table

        Args: 
            new_trash: A new trash that admin has input 

        Returns:
            A dictionary contains the data that has been input to the table, and success status code
        """
        parser = reqparse.RequestParser()

        parser.add_argument('trash_category_id',
                            location='json', type=int, required=True)
        parser.add_argument('trash_name', location='json', required=True)
        parser.add_argument('price', location='json', type=int, required=True)
        parser.add_argument('photo', location='json')
        parser.add_argument('point', location='json', type=int, required=True)

        args = parser.parse_args()

        new_trash = {
            'trash_category_id': args['trash_category_id'],
            'trash_name': args['trash_name'],
            'price': args['price'],
            'photo': args['photo'],
            'point': args['point']
        }

        trash = ListTrash(new_trash)
        db.session.add(trash)
        db.session.commit()

        app.logger.debug('DEBUG : %s', trash)

        return marshal(trash, ListTrash.response_fields), 200, {'Content_Type': 'application/json'}

    @jwt_required
    def get(self):

        trashes = ListTrash.query

        trashes_list = []
        for trash in trashes:
            trash = marshal(trash, ListTrash.response_fields)
            trashes_list.append(trash)

        return trashes_list, 200, {'Content_Type': 'application/json'}

    @adminRequired
    def put(self, id):

        parser = reqparse.RequestParser()

        parser.add_argument('trash_category_id', location='json', type=int)
        parser.add_argument('trash_name', location='json')
        parser.add_argument('price', location='json', type=int)
        parser.add_argument('photo', location='json')
        parser.add_argument('point', location='json', type=int)

        args = parser.parse_args()
        trash = ListTrash.query.get(id)

        if trash is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        if args['trash_category_id'] is not None:
            trash.trash_category_id = args['trash_category_id']
        if args['trash_name'] is not None:
            trash.trash_name = args['trash_name']

        if args['price'] is not None:
            trash.price = args['price']

        if args['photo'] is not None:
            trash.photo = args['photo']

        if args['point'] is not None:
            trash.point = args['point']

        trash.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        return marshal(trash, ListTrash.response_fields), 200, {'Content_Type': 'application/json'}

    @adminRequired
    def delete(self, id):
        trash = ListTrash.query.get(id)

        if trash is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        db.session.delete(trash)
        db.session.commit()
        return {"Status": "The data with id {} is deleted".format(id)}, 200, {'Content_Type': 'application/json'}


api.add_resource(TrashResource, '', '/<id>')
