import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from sqlalchemy import desc
from .model import ListOrders
from apps.order_details.model import ListOrderDetails
from apps.trashes.model import ListTrash
from apps.user_attributes.model import UserAttributes
from apps.users.model import Users
from apps import db, app
from flask_jwt_extended import jwt_required, get_jwt_claims
from apps import adminRequired, userRequired

bp_orders = Blueprint('orders', __name__)
api = Api(bp_orders)


class OrdersResource(Resource):
    """Class for storing HTTP request method for ordes table"""

    def addDetails(self, arr, order, attr):
        """function to add order details to order details table
        also update order and user attribute table

        Args (located in function's parameters):
          arr: An array of order detail dictionary
          order: the order which want to be updated with details
          user_attr: user attributes which later will be updated
        """
        for detail in arr:

            trash = ListTrash.query.get(detail['trash_id'])
            trash = marshal(trash, ListTrash.response_fields)

            total_price = int(trash['price'] * detail['qty'])
            point = int(detail['qty']) * trash['point']

            # make a new order detail instance

            new = detail.update(
                {"order_id": int(order.id), "total_price": total_price, "point": point})
            new_detail = ListOrderDetails(detail)

            # updating the order's total_qty, total_price, total_point, and status

            order.total_qty += detail['qty']
            order.total_price += total_price
            order.total_point += point

            # update corresponding user's attribute

            attr.total_trash += detail['qty']
            attr.point += point

            # add order detail to database, and commit all changes and update

            db.session.add(new_detail)
            db.session.commit()

    def __init__(self):
        """Init function needed to indicate this is a class, but never used"""
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return {"Status": "ok"}, 200

    @userRequired
    def post(self):
        """Post new data to orders table

        Retrieve data from user input located in JSON and from user's jwt claims

        Args:
            adress: A string of order's pick up location (located in JSON)
            time: A datetime of order's pick up time (located in JSON)
            photo: A string of user's trash' photo's url (located in JSON)
            user_id: An integer of user's id (retrieve from jwt claims)
            status: set to be 'waiting' (manually inserted)

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "id": 1,
                "user_id": 1,
                "admin_id": null,
                "adress": "Jl. Bunga No. 30, Sukun, Malang",
                "time": Tue, 20 Jan 2019 09:30:00-0000,
                "photo": "imurl.com/folder/image.jpg",
                "status": "waiting",
                "total_qty": 5.1,
                "total_price": 5100,
                "total_point": 5,
                "created_at": Tue, 20 Jan 2019 09:30:00-0000
            }

        Raises: 
            Forbidden (403): An error that occured when admin try to post a new order         
        """
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()

        parser.add_argument('adress', location='json', required=True)
        parser.add_argument('time', location='json')
        parser.add_argument('photo', location='json')

        args = parser.parse_args()

        new_order = {
            "user_id": claims['id'],
            "adress": args['adress'],
            "time": args['time'],
            "photo": args['photo'],
            "status": 'waiting'
        }

        order = ListOrders(new_order)
        db.session.add(order)
        db.session.commit()

        app.logger.debug('DEBUG : %s', order)

        return marshal(order, ListOrders.response_fields), 200, {'Content_Type': 'application/json'}

    @jwt_required
    def put(self, id):
        """Update orders table with new status and/or add order details to database.
        process and response depend on user role (admin or non-admin)

        Args (located in JSON):
            status: string of order's status. it could be waiting or cancelled (can be inputted by only standard user), or rejected,confirmed,or done(can be inputted only by admin)
            details: An array of order details dictionaries that later will be added to database if the status above is 'done'

        Returns:
            If the status is 'done', will returns a dictionary with key 'details_added' and value an array of dictionaries of order details from corresponding order. For example :
            {
                "details_added":[
                {
                    "id": 1,
                    "order_id": 2,
                    "trash_id": 1,
                    "qty": 2.9,
                    "total_price": 2900,
                    "point": 2,
                    "created_at": "Sun, 15 Sep 2019 20:16:55-0000"
                },
                {
                    "id": 2,
                    "order_id": 2,
                    "trash_id": 2,
                    "qty": 4,
                    "total_price": 2000,
                    "point": 4,
                    "created_at": "Sun, 15 Sep 2019 20:16:55 -0000"
                }
            ]
            }


            Otherwise, will returns a dictionary of updated data from corresponding order. For example :
            {
                "id": 1,
                "user_id": 1,
                "admin_id": 2,
                "adress": "Jl. Bunga No. 30, Sukun, Malang",
                "time": Tue, 20 Jan 2019 09:30:00-0000,
                "photo": "imurl.com/folder/image.jpg",
                "status": "cancelled",
                "total_qty": 5.1,
                "total_price": 5100,
                "total_point": 5,
                "created_at": Tue, 20 Jan 2019 09:30:00-0000
            }

        Raise:
            Forbidden(403): An error that occured when a user put with status that is not permitted. As an example when an admin try to put with status 'cancelled', or when a user try to put with status 'confirmed'. 
            Not Found(404): An error that occured when a user try to update unavailable data.
        """
        user = get_jwt_claims()
        user_status = user['role']

        parser = reqparse.RequestParser()

        choices = ('waiting', 'rejected', 'cancelled', 'done', 'confirmed')
        parser.add_argument('status', location='json',
                            required=True, choices=choices)
        parser.add_argument('details', location='json', type=list)

        args = parser.parse_args()

        order = ListOrders.query.get(id)

        if order is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        # If the status inputted is not 'done', the user role will be checked.
        # Return a warning if the role is not suitable with the status, or commit change if the role is suitable

        if args['status'] == 'cancelled':
            if user['role']:
                return {'Warning': 'Only User can cancel'}, 403, {'Content_Type': 'application/json'}
            order.status = 'cancelled'
            db.session.commit()
            return marshal(order, ListOrders.response_fields), 200, {'Content_Type': 'application/json'}

        if args['status'] == 'confirmed':
            if not user['role']:
                return {'Warning': 'Only admin can confirm'}, 403, {'Content_Type': 'application/json'}
            order.status = 'confirmed'
            order.admin_id = user['id']
            db.session.commit()
            return marshal(order, ListOrders.response_fields), 200, {'Content_Type': 'application/json'}

        if args['status'] == 'rejected':
            if not user['role']:
                return {'Warning': 'Only admin can reject'}, 403, {'Content_Type': 'application/json'}
            order.status = 'rejected'
            order.admin_id = user['id']
            db.session.commit()
            return marshal(order, ListOrders.response_fields), 200, {'Content_Type': 'application/json'}

        # if the status is 'done' and inputted by admin, both order and order_details table will be updated in addDeatails function

        if args['status'] == 'done':
            if not user['role']:
                return {'Warning': 'Only Admin can change status to done'}, 403, {'Content_Type': 'application/json'}
            order_dict = marshal(order, ListOrders.response_fields)

            user_attr = UserAttributes.query.filter_by(
                user_id=order_dict['user_id']).first()

            details = args['details']
            self.addDetails(details, order, user_attr)

            order.status = 'done'
            order.admin_id = user['id']
            db.session.commit()

            return {"details_added": details}, 200, {'Content_Type': 'application/json'}

    @adminRequired
    def get(self):
        """Get all the order data from orders table

        Returns:
            An array of dictionaries consist of orders data. For example:
            [
                {
                    "id": 1,
                    "user_id": 1,
                    "admin_id": 2,
                    "adress": "Jl. Bunga No. 30, Sukun, Malang",
                    "time": Tue, 20 Jan 2019 09:30:00-0000,
                    "photo": "imurl.com/folder/image.jpg",
                    "status": "waiting",
                    "total_qty": 5.1,
                    "total_price": 5100,
                    "total_point": 5,
                    "created_at": Tue, 20 Jan 2019 09:30:00-0000
                },
                {
                    "id": 2,
                    "user_id": 2,
                    "admin_id": 2,
                    "adress": "Jl. Bunga No. 30, Sukun, Malang",
                    "time": Tue, 20 Jan 2019 09:30:00-0000,
                    "photo": "imurl.com/folder/image2.jpg",
                    "status": "waiting",
                    "total_qty": 5.1,
                    "total_price": 5100,
                    "total_point": 5,
                    "created_at": Tue, 20 Jan 2019 09:31:00-0000
                }    
            ]

        Raise:
            Forbidden(403): An error occured when this function accessed by user
        """
        orders = ListOrders.query.order_by(ListOrders.id.desc())
        order_list = []
        for order in orders:
            order = marshal(order, ListOrders.response_fields)
            details = ListOrderDetails.query.filter_by(order_id=order['id'])
            user = Users.query.get(order['user_id'])
            user = marshal(user, Users.response_fields)
            details_dict = []
            for detail in details:
                detail = marshal(detail, ListOrderDetails.response_fields)
                trash = ListTrash.query.get(detail['trash_id'])
                trash_detail = marshal(trash, ListTrash.response_fields)
                new = detail.update({'trash_detail': trash_detail})
                details_dict.append(detail)

            order_with_detail = {"Order": order,
                                 "Details": details_dict, "User": user}
            order_list.append(order_with_detail)

        return order_list, 200, {'Content_Type': 'application/json'}


class UserOrdersResource(Resource):
    """Class for storing HTTP request method that accessed by user for ordes table"""

    def __init__(self):
        """Init function needed to indicate this is a class, but never used"""
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return {"Status": "ok"}, 200

    @userRequired
    def get(self):
        """Get all order made by a specific user whose id was taken from jwt claims

        Returns: An array of dictionaries consist of orders data from corresponding user. For example:
            [
                {
                    "id": 2,
                    "user_id": 1,
                    "admin_id": 2,
                    "adress": "Jl. Bunga No. 30, Sukun, Malang",
                    "time": Tue, 20 Jan 2019 09:30:00-0000,
                    "photo": "imurl.com/folder/image.jpg",
                    "status": "waiting",
                    "total_qty": 5.1,
                    "total_price": 5100,
                    "total_point": 5,
                    "created_at": Tue, 20 Jan 2019 09:30:00-0000
                },
                {
                    "id": 2,
                    "user_id": 2,
                    "admin_id": 2,
                    "adress": "Jl. Bunga No. 30, Sukun, Malang",
                    "time": Tue, 20 Jan 2019 09:30:00-0000,
                    "photo": "imurl.com/folder/image2.jpg",
                    "status": "waiting",
                    "total_qty": 5.1,
                    "total_price": 5100,
                    "total_point": 5,
                    "created_at": Tue, 20 Jan 2019 09:31:00-0000
                }    
            ]

        Raise:
            Forbidden(403): An error occured when this function accessed by user
        """

        user = get_jwt_claims()
        orders = ListOrders.query.filter_by(
            user_id=user['id']).order_by(ListOrders.id.desc())
        order_list = []
        for order in orders:
            order = marshal(order, ListOrders.response_fields)
            details = ListOrderDetails.query.filter_by(order_id=order['id'])
            details_dict = []
            for detail in details:
                detail = marshal(detail, ListOrderDetails.response_fields)
                trash = ListTrash.query.get(detail['trash_id'])
                trash_detail = marshal(trash, ListTrash.response_fields)
                new = detail.update({'trash_detail': trash_detail})
                details_dict.append(detail)

            order_with_detail = {"Order": order,
                                 "Details": details_dict, "User": user}
            order_list.append(order_with_detail)

        return order_list, 200, {'Content_Type': 'application/json'}


api.add_resource(OrdersResource, '', '/<id>')
api.add_resource(UserOrdersResource, '/user')
