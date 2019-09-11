from apps import db
from flask_restful import fields
import datetime


class ListOrderDetails(db.Model):
    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, nullable = False)
    trash_id = db.Column(db.Integer, nullable = False)
    qty = db.Column(db.Float, nullable = False)
    total_price = db.Column(db.Integer, nullable = False)
    point = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)

    response_fields = {
        'id': fields.Integer,
        'order_id' : fields.Integer,
        'trash_id' : fields.Integer,
        'qty' : fields.Float,
        'total_price' : fields.Integer,
        'point' : fields.Integer,
        'created_at' : fields.DateTime
    }

    def __init__(self, data):
      self.order_id = data['order_id']
      self.trash_id = data['trash_id']
      self.qty = data['qty']
      self.total_price = data['total_price']
      self.point = data['point']
            
