from apps import db
from flask_restful import fields
import datetime


class ListOrderDetails(db.Model):
    """Class for storing information about Order details table

    Attributes:
        __tablename__: a string of table name
        id: an integer of order details' id
        order_id: an integer of order id which detail is in the corresponding row
        trash_id: an integer of trash_id
        qty: a number of trash' total wight(in kilograms)
        total_price: an integer of total price of the trash(in Rupiah)
        role: an Integer of point a user get from the corresponding transaction detail
        created_at: a datetime that indicates when the detail created
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    trash_id = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'order_id': fields.Integer,
        'trash_id': fields.Integer,
        'qty': fields.Float,
        'total_price': fields.Integer,
        'point': fields.Integer,
        'created_at': fields.DateTime
    }

    def __init__(self, data):
        """Inits Order details with data that inputted

        Args:
            data: a dictionary contain key and value pairs described below
                    order_id: an integer of order's id
                    trash_id: an integer of trash's id
                    qty: a number of trash' total weight
                    total_price: an integer of total price of the trash
                    point: an integer of point that user get from corresponding transaction detail
        """
        self.order_id = data['order_id']
        self.trash_id = data['trash_id']
        self.qty = data['qty']
        self.total_price = data['total_price']
        self.point = data['point']
