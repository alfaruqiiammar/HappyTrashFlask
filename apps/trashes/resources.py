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
    """Class for storing HTTP request method for users table that can be accessed by user"""

    def __init__(self):
        """Init function needed to indicate this is a class"""
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return {"status": "Ok"}, 200

    @adminRequired
    def post(self):
        """ Post a new trash to trashes table

        Args:
            admin_id: an integer of admin's id (retrieved from jwt claims)
            trash_category_id: An integer of trash category's id (located in JSON)
            trash_name: A string of trash name (located in JSON)
            price: An integer of trash price per kilogram (located in JSON)
            photo:  A string of trash' photo's url (located in JSON)
            point: an integer which indicates the amount of point a user will get per kilogram of corresponding trash (located in JSON)

        Returns:
            A dictionary contains the data that has been input to the table. For example:
            {
                "id":1,
                "admin_id": 2,
                "trash_category_id": 2,
                "trash_name": "plastik PE",
                "price": 1000,
                "photo": "imurl/folder/image.png",
                "point": 5,
                "created_at": Sat, 26 Apr 2019 09:00:00 -000
                "updated_at": Sat, 26 Apr 2019 09:00:00 -000 
            }

        Raises:
            Forbidden(403): an error occured when non-admin user try to post a new trash
        """
        parser = reqparse.RequestParser()

        parser.add_argument('trash_category_id',
                            location='json', type=int, required=True)
        parser.add_argument('trash_name', location='json', required=True)
        parser.add_argument('price', location='json', type=int, required=True)
        parser.add_argument('photo', location='json')
        parser.add_argument('point', location='json', type=int, required=True)

        args = parser.parse_args()

        admin = get_jwt_claims()

        new_trash = {
            'admin_id': admin['id'],
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
        """Get all data from the trashes table

        Returns:
            An array of dictionaries consist of trash data. For example:
            [
                {
                    "id":2,
                    "admin_id" : 2,
                    "trash_category_id": 2,
                    "trash_name": "plastik PE",
                    "price": 1000,
                    "photo": "imurl/folder/image.png",
                    "point": 5,
                    "created_at": Sat, 26 Apr 2019 09:00:00 -000
                    "updated_at": Sat, 26 Apr 2019 09:00:00 -000 
                },
                {
                    "id":1,
                    "admin_id" : 2,
                    "trash_category_id": 3,
                    "trash_name": "Gelas kaca",
                    "price": 1000,
                    "photo": "imurl/folder/image.png",
                    "point": 5,
                    "created_at": Sat, 26 Apr 2019 09:00:00 -000
                    "updated_at": Sat, 26 Apr 2019 09:00:00 -000 
                }   
            ]

        Raises:
            Unauthorized(401): an error occured when unauthorized user try to use this function
        """
        trashes = ListTrash.query.order_by(ListTrash.id.desc())

        trashes_list = []
        for trash in trashes:
            trash = marshal(trash, ListTrash.response_fields)
            trashes_list.append(trash)

        return trashes_list, 200, {'Content_Type': 'application/json'}

    @adminRequired
    def put(self, id):
        """ Edits category_name from a single record in trash_category table specified by id 

        Args: 
            admin_id: An integer of admin's id (retrieved from jwt claims)
            trash_category_id: An integer of trash category's id (located in JSON)
            trash_name: A string of trash name (located in JSON)
            price: An integer of trash price per kilogram (located in JSON)
            photo:  A string of trash' photo's url (located in JSON)
            point: an integer which indicates the amount of point a user will get per kilogram of corresponding trash (located in JSON)
            status: a boolean which indicates status of the trash, True for active, or false for inactive

        Returns:
            A dictionary that contains the updated data from the record edited. For example:
            {
                "id":1,
                "admin_id": 2,
                "trash_category_id": 2,
                "trash_name": "plastik PE",
                "price": 1000,
                "photo": "imurl/folder/image.png",
                "point": 5,
                "status": False
                "created_at": Sat, 26 Apr 2019 09:00:00 -000
                "updated_at": Sat, 26 Apr 2019 09:50:00 -000 
            }

        Raise:
            Not Found(404): An error occured when the id inputted is not found in the table
        """
        parser = reqparse.RequestParser()

        parser.add_argument('trash_category_id', location='json', type=int)
        parser.add_argument('trash_name', location='json')
        parser.add_argument('price', location='json', type=int)
        parser.add_argument('photo', location='json')
        parser.add_argument('point', location='json', type=int)
        parser.add_argument('status', location='json', type=inputs.boolean)

        args = parser.parse_args()
        trash = ListTrash.query.get(id)

        admin = get_jwt_claims()

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

        if args['status'] is not None:
            trash.status = args['status']

        trash.admin_id = admin['id']

        db.session.commit()
        return marshal(trash, ListTrash.response_fields), 200, {'Content_Type': 'application/json'}

    @adminRequired
    def delete(self, id):
        """Delete a single record from trashes table

        Args (located in function's parameter) : 
            id: An integer of trash' id which want to be deleted

        Returns:
            A dictionary of key 'status' which have value of sucess message. For example:
            {"Status": "The data with id 3 is deleted"}

        Raise:
            Not Found(404): An error occured when the id inputted is not found in the table
        """
        trash = ListTrash.query.get(id)
        admin = get_jwt_claims()

        if trash is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        db.session.delete(trash)
        db.session.commit()
        return {"Status": "The data with id {} is deleted".format(id)}, 200, {'Content_Type': 'application/json'}


api.add_resource(TrashResource, '', '/<id>')
