from apps import db
from flask_restful import fields
import datetime


class ListOrders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    adress = db.Column(db.String(225), nullable = False)
    time = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    photo = db.Column(db.String(500))
    status = db.Column(db.String(20), nullable = False)
    total_qty = db.Column(db.Integer, default = 0)
    total_price = db.Column(db.Integer, default = 0)
    total_point = db.Column(db.Integer, default = 0)
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)

    response_fields = {
        'id': fields.Integer,
        'user_id' : fields.Integer,
        'adress' : fields.String,
        'time' : fields.DateTime,
        'photo' : fields.String,
        'status' : fields.String,
        'total_qty' : fields.Integer,
        'total_price' : fields.Integer,
        'total_point' : fields.Integer,
        'created_at' : fields.DateTime
    }

    def __init__(self, data):
      self.user_id = data['user_id']
      self.adress = data['adress']
      self.time = data['time']
      self.photo = data['photo']
      self.status = data['status']
            
