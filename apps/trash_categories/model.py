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

    def __init__(self, category_name):
        self.category_name = category_name

