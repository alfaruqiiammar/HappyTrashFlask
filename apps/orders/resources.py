import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from sqlalchemy import desc
from .model import ListOrders
from apps.order_details.model import ListOrderDetails
from apps.trashes.model import ListTrash
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
  
  # @userRequired
  def post(self):
    # claims = get_jwt_claims()
    parser = reqparse.RequestParser()

    parser.add_argument('adress', location='json', required = True)
    parser.add_argument('time', location='json')
    parser.add_argument('photo', location = 'json')

    args = parser.parse_args()

    new_order = {
      # "user_id" : claims['id'] ,
      "user_id" : 1,
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

  # @adminRequired
  def put(self, id):
    """
    takes 2 argument from user
    status
    details
    penjelasan details :
    berisi qty dan trash_id
    """
    parser = reqparse.RequestParser()

    parser.add_argument('status', location='json', required = True)
    parser.add_argument('details', location='json', type = list)

    args = parser.parse_args()

    order = ListOrders.query.get(id)

    if order is None:
      return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}
    
    if args['status'] == 'cancelled':
      order.status = 'cancelled'
      db.session.commit()
      return marshal(order, ListOrders.response_fields), 200, {'Content_Type': 'application/json'}
    
    if args['status'] == 'done':
      details = args['details']
      for detail in details:
        trash = ListTrash.query.get(detail['trash_id'])
        trash = marshal(trash,ListTrash.response_fields)
        total_price = int(trash['price'] * detail['qty'])
        order.total_qty += detail['qty']
        point = int(detail['qty'] * trash['point'])
        new = detail.update({"order_id" : int(id), "total_price" : total_price, "point" : point})
        new_detail = ListOrderDetails(detail)
        db.session.add(new_detail)
        order.total_qty += detail['qty']
        order.total_price += total_price
        order.total_point += point
        order.status = 'done'
        db.session.commit() 
      order.status = 'done'
      db.session.commit()
      return {"details_added" : details }, 200, {'Content_Type': 'application/json'}



  def get(self):
    pass

api.add_resource(OrdersResource, '', '/<id>')
  
