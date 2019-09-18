from apps import db
from flask_restful import fields
import datetime


class ListTrash(db.Model):
    """Class for storing information about trash

    Attributes:
        __tablename__: a string of table name
        id: an integer of trash' id
        admin_id: an integer of admin's id
        trash_category_id: an integer of trash category's id
        trash_name: a string of trash' name
        price: an integer of trash price per kilogram
        photo: a string of trash' photo's url
        point: an integer which indicates the amount of point a user will get per kilogram of corresponding trash
        status: a boolean that indicates category status. True for active and False for inactive
        date_created: a datetime that indicates when the record created
        date_updated: a datetime that indicates when the record last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "trashes"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, nullable=False)
    trash_category_id = db.Column(db.Integer, nullable=False)
    trash_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(500))
    point = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    response_fields = {
        'id': fields.Integer,
        'admin_id': fields.Integer,
        'trash_category_id': fields.Integer,
        'trash_name': fields.String,
        'price': fields.Integer,
        'photo': fields.String,
        'point': fields.Integer,
        'status': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, data):
        """Inits a trash record with the data inputted

        Args: 
            data: a dictionary of trash' attribute. For example:
                    {
                        "trash_category_id": 2,
                        "trash_name": "plastik PE",
                        "price": 1000,
                        "photo": "imurl/folder/image.png",
                        "point": 5
                    }
        """
        self.admin_id = data['admin_id']
        self.trash_category_id = data['trash_category_id']
        self.trash_name = data['trash_name']
        self.price = data['price']
        self.photo = data['photo']
        self.point = data['point']
