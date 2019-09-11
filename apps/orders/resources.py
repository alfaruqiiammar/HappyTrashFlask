import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from sqlalchemy import desc
from .model import ListOrders
from apps import db,app
from flask_jwt_extended import jwt_required, get_jwt_claims
from apps import adminRequired, userRequired

bp_orders = Blueprint('orders', __name__)
api = Api(bp_orders)

class OrdersResource(Resource):

  def __init__(self):
    pass
  
  def options(self, id=None):
    return {"Status" : "ok"}, 200
  
  @userRequired
  def post(self):
    claims = get_jwt_claims()
    parser = reqparse.RequestParser()

    parser.add_argument('adress', location='json', required = True)
    parser.add_argument('time', location='json')
    parser.add_argument('photo', location = 'json')

    args = parser.parse_args()

    new_order = {
      "user_id" : claims['id'] ,
      "adress" : args['adress'],
      "time" : args['time'],
      "photo" : args['photo'],
      "status" : 'waiting'
    }

    order = ListOrders(new_order)
    db.session.add(order)
    db.session.commit()

    app.logger.debug('DEBUG : %s', order)

    return marshal(order, ListOrders.response_fields), 200, {'Content_Type' : 'application/json'}

  def put(self, id):
    pass

  def get(self):
    pass

api.add_resource(OrdersResource, '', '/<id>')
  
