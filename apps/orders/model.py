from apps import db
from flask_restful import fields
import datetime


class ListOrders(db.Model):
    """Class for storing information about orders table

    Attributes:
        __tablename__: a string of table name
        id: an integer of order's id
        user_id : an integer of user's id,
        admin_id : an integer of admin's id
        adress : a string that indicates where the pick-up adress is,
        time : a datetime that indicates when the user want their trash to be picked,
        photo : a url of user's trash picture,
        status : a string that indicates the status of the order. it can be waiting, cancelled, or done,
        total_qty : float that indicates the total weight of the trash, set to be 0 at first,
        total_price : integer that indicates the total price of the trash,
        total_point : integer that indicates the total point user gets after the transaction,
        date_created: a datetime that indicates when the order created
        date_updated: a datetime that indicates when the order last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, nullable=True)
    adress = db.Column(db.String(225), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    photo = db.Column(db.String(500))
    status = db.Column(db.String(20), nullable=False)
    total_qty = db.Column(db.Float, default=0)
    total_price = db.Column(db.Integer, default=0)
    total_point = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'admin_id': fields.Integer
        'adress': fields.String,
        'time': fields.DateTime,
        'photo': fields.String,
        'status': fields.String,
        'total_qty': fields.Float,
        'total_price': fields.Integer,
        'total_point': fields.Integer,
        'created_at': fields.DateTime
    }

    def __init__(self, data):
        """
        Inits Order with data inputted

        Args :
            data: a dictionary contain key: value pairs described below
            user_id : an integer of user's id,
            adress : a string that indicates where the pick-up adress is,
            time : a datetime that indicates when the user want their trash to be picked,
            photo : a url of user's trash picture,
            status : a string that indicates the status of the order. it can be waiting, cancelled, or done,
        """
        self.user_id = data['user_id']
        self.admin_id = data['admin_id']
        self.adress = data['adress']
        self.time = data['time']
        self.photo = data['photo']
        self.status = data['status']
