from apps import db
from flask_restful import fields
import datetime


class ListTrash(db.Model):
    __tablename__ = "trashes"

    id = db.Column(db.Integer, primary_key=True)
    trash_category_id = db.Column(db.Integer, nullable=False)
    trash_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(500))
    point = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    response_fields = {
        'id': fields.Integer,
        'trash_category_id': fields.Integer,
        'trash_name': fields.String,
        'price': fields.Integer,
        'photo': fields.String,
        'point': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, data):
        self.trash_category_id = data['trash_category_id']
        self.trash_name = data['trash_name']
        self.price = data['price']
        self.photo = data['photo']
        self.point = data['point']
