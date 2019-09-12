from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Rewards
from sqlalchemy import desc
from apps import app, db
from flask_jwt_extended import jwt_required, get_jwt_claims
from apps import adminRequired, userRequired

bp_rewards = Blueprint('rewards', __name__)
api = Api(bp_rewards)

class RewardsResource(Resource):
    """Class for storing HTTP request method for rewards table"""

    def __init__(self):
        """Init function needed to indicate this is a class, but never used"""
        pass

    def options(self, id):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return {'Status': 'OK'}, 200	

    @jwt_required
    @adminRequired
    def post(self):
        """Post new data to rewards table

        Retrieve data from admin input located in JSON, validate the data, then post the data to rewards tables.

        Args (located in JSON):
            name: a string of reward's name
            point_to_claim: an integer that indicates amount points needed to claim the rewards
            photo: a string of reward's photo
            stock: an integer that indicates amount of stock available
            status: a boolean that indicates reward status. True for active and False for inactive

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "name": "voucher sepulsa 20rb",
                "point_to_claim: 20,
                "photo": "http://images.squarespace-cdn.com/content/v1/551dcbdae4b0827b21732cc8/1513122056011-K43Y8ZQB0DADG60YR0L6/ke17ZwdGBToddI8pDm48kJz9WYGIhFMDCoO5TzZfZDZ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UQ8mheSOtvJ3ZKSxxLOkTv9WG-IdheQ6w_cTdjvdSdKGMItJCPe_onvT9kHS8V4I0Q/voucher.jpg"
                "stock": 100,
                "status": True
            }
        
        Raises: 
            Bad Request (400): An error that occured when some of the field is missing, or if the data is not valid, or if the data inputted is already listed on database
        """

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json', required=True)
        parser.add_argument('point_to_claim', type=int, location='json', required=True)
        parser.add_argument('photo', type=str, location='json', required=True)
        parser.add_argument('stock', type=int, location='json', required=True)
        parser.add_argument('status', type=bool, location='json', required=True)
        args = parser.parse_args()

        # Input data to rewards table

        reward = Rewards(args['name'], args['point_to_claim'], args['photo'], args['stock'], args['status'])

        db.session.add(reward)
        db.session.commit()

        app.logger.debug('DEBUG : %s', reward)

        return marshal(reward, Rewards.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @adminRequired
    def get(self):
        """Get all data from rewards table

        Returns:
            A list of dicts mapping keys to the corresponding value, for example:

            [
                {
                    "id": 1,
                    "name": "voucher sepulsa 20rb",
                    "point_to_claim": 20,
                    "photo": "http://images.squarespace-cdn.com/content/v1/551dcbdae4b0827b21732cc8/1513122056011-K43Y8ZQB0DADG60YR0L6/ke17ZwdGBToddI8pDm48kJz9WYGIhFMDCoO5TzZfZDZ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UQ8mheSOtvJ3ZKSxxLOkTv9WG-IdheQ6w_cTdjvdSdKGMItJCPe_onvT9kHS8V4I0Q/voucher.jpg",
                    "stock": 100,
                    "status": true
                },
                {
                    "id": 2,
                    "name": "voucher sepulsa 50rb",
                    "point_to_claim": 20,
                    "photo": "http://images.squarespace-cdn.com/content/v1/551dcbdae4b0827b21732cc8/1513122056011-K43Y8ZQB0DADG60YR0L6/ke17ZwdGBToddI8pDm48kJz9WYGIhFMDCoO5TzZfZDZ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UQ8mheSOtvJ3ZKSxxLOkTv9WG-IdheQ6w_cTdjvdSdKGMItJCPe_onvT9kHS8V4I0Q/voucher.jpg",
                    "stock": 100,
                    "status": true
                }
            ]
        """

        rewards = Rewards.query

        rewards_list = []
        for reward in rewards:
            reward = marshal(reward, Rewards.response_fields)
            rewards_list.append(reward)

        return rewards_list, 200, {'Content_Type': 'application/json'}

    
    def put(self, id):
        """Change rewards's field data by data inputted by admin

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "id": 1,
                "name": "voucher sepulsa 20rb",
                "point_to_claim": 20,
                "photo": "http://images.squarespace-cdn.com/content/v1/551dcbdae4b0827b21732cc8/1513122056011-K43Y8ZQB0DADG60YR0L6/ke17ZwdGBToddI8pDm48kJz9WYGIhFMDCoO5TzZfZDZ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UQ8mheSOtvJ3ZKSxxLOkTv9WG-IdheQ6w_cTdjvdSdKGMItJCPe_onvT9kHS8V4I0Q/voucher.jpg",
                "stock": 100,
                "status": true
            }
        """

        parser = reqparse.RequestParser()

        parser.add_argument('name', type=str, location='json')
        parser.add_argument('point_to_claim', type=int, location='json')
        parser.add_argument('photo', type=str, location='json')
        parser.add_argument('stock', type=int, location='json')
        parser.add_argument('status', type=bool, location='json')

        args = parser.parse_args()
        reward = Rewards.query.get(id)
        reward_contain = marshal(reward, Rewards.response_fields)

        if reward is None:
            return {'status': 'Reward Not Found'}, 404, {'Content_Type': 'application/json'}

        if args['name'] is not None:
            reward.name = args['name']
            
        if args['point_to_claim'] is not None:
            reward.point_to_claim = args['point_to_claim']

        if args['photo'] is not None:
            reward.photo = args['photo']

        if args['stock'] is not None:
            reward.stock = args['stock']

        if args['status'] is not None:
            reward.status = args['status']

        db.session.commit()
        return marshal(reward, Rewards.response_fields), 200, {'Content_Type': 'application/json'}

api.add_resource(RewardsResource, '', '/<id>')