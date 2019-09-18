from apps import db
from flask_restful import fields
import datetime


class ListTrashCategory(db.Model):
    """Class for storing information about trash categories

    Attributes:
        __tablename__: a string of table name
        id: an integer of category's id
        admin_id: an integer of admin's id
        category_name: a string of category's name
        status: a boolean that indicates category status. True for active and False for inactive
        date_created: a datetime that indicates when the record created
        date_updated: a datetime that indicates when the record last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "trash_categories"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, nullable=False)
    category_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    response_fields = {
        'id': fields.Integer,
        'admin_id': fields.Integer,
        'category_name': fields.String,
        'status': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, admin_id, category_name):
        """Inits a category with the name inputted

        Args:
            admin_id: an integer of admin's id
            category_name: a string of category's name
        """
        self.category_name = category_name
        self.admin_id = admin_id
