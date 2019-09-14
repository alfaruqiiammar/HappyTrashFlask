from apps import db
from flask_restful import fields
import re


class Rewards(db.Model):
    """Class for storing information about rewards table

    Attributes:
        __tablename__: a string of table name
        id: an integer of rewards's id
        name: a string of reward's name
        point_to_claim: an integer that indicates amount points needed to claim the rewards
        photo: a string of reward's photo
        stock: an integer that indicates amount of stock available
        status: a boolean that indicates reward status. True for active and False for inactive
        date_created: a datetime that indicates when the account created
        date_updated: a datetime that indicates when the account last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "rewards"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    point_to_claim = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(1000), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'point_to_claim': fields.Integer,
        'photo': fields.String,
        'stock': fields.Integer,
        'status': fields.Boolean,
        'date_created': fields.DateTime,
        'date_modified': fields.DateTime
    }

    def __init__(self, name, point_to_claim, photo, stock, status):
        """Inits Rewards with data that admin inputted

        The data already validated on the resources function

        Args:
            name: a string of reward's name
            point_to_claim: an integer that indicates amount points needed to claim the rewards
            photo: a string of reward's photo
            stock: an integer that indicates amount of stock available
            status: a boolean that indicates reward status. True for active and False for inactive
        """
        self.name = name
        self.point_to_claim = point_to_claim
        self.photo = photo
        self.stock = stock
        self.status = status
