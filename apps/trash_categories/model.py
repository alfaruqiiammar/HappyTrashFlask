from apps import db
from flask_restful import fields
import datetime


class ListTrashCategory(db.Model):
    __tablename__ = "trash_categories"

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    response_fields = {
        'id': fields.Integer,
        'category_name': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, data):
        self.category_name = data['category_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
