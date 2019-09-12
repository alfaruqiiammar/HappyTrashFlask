from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from .model import RewardHistories
# from apps.rewards.model import Rewards
from sqlalchemy import desc
from apps import app, db, userRequired, adminRequired
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_reward_histories = Blueprint('reward_histories', __name__)
api = Api(bp_reward_histories)

class AdminRewardHistoriesResource(Resource):
  """Class for storing HTTP request method for reward_histories table, accessed by admin"""
  def __init__(self):
    pass

  def options(self, id = None):
    return {'Status': 'OK'}, 200
    
  @adminRequired
  def get(self):
    """Get all reward_histories from table
    Returns :
      An array of dictionaries, for example:

      [
        {
          "id": 1,
          "reward_id": 1,
          "reward_name": "voucher 10k",
          "user_id": 1,
          "created_at": "2019-09-12 07:26:21"
        },
        {
          "id": 2,
          "reward_id": 1,
          "reward_name": "voucher 10k",
          "user_id": 3,
          "created_at": "2019-09-12 07:26:21"          
        }
      ]
    """
    histories = RewardHistories.query
    histories_list = []

    for history in histories:
      history = marshal(history, RewardHistories.response_fields)
      histories_list.append(history)
    
    return histories_list, 200, {'Content_Type': 'application/json'}

class UserRewardHistoriesResource(Resource):
  """Class for storing HTTP request method for reward_histories table, accessed by user"""
  def __init__(self):
    pass

  def options(self):
    return {'Status': 'OK'}, 200
  
  @userRequired
  def get(self):
    """Get all reward_histories of a specific user
    Returns :
      An array of dictionaries, for example:

      [
        {
          "id": 1,
          "reward_id": 1,
          "reward_name": "voucher 10k",
          "user_id": 1,
          "created_at": "2019-09-12 07:26:21"
        },
        {
          "id": 2,
          "reward_id": 2,
          "reward_name": "voucher 20k",
          "user_id": 1,
          "created_at": "2019-09-12 07:26:21"          
        }
      ]
    """
    user = get_jwt_claims()
    histories = RewardHistories.query.filter_by(user_id = user['id'])
    histories_list = []

    for history in histories:
      history = marshal(history, RewardHistories.response_fields)
      histories_list.append(history)
    
    return histories_list, 200, {'Content_Type': 'application/json'}
  
  @userRequired
  def post(self):
    """Post a new data to reward history table
    Args:
      reward_id : located in json
      reward_name : rewards name from id above, located in rewards table
      user_id : located in json
    """

    user = get_jwt_claims()
    parser = reqparse.RequestParser()
    parser.add_argument('reward_id', location = 'json', required = True)
    parser.add_argument('reward_name', location = 'json', required = True)

    args = parser.parse_args()

    new_history = {
      'reward_id' : args['reward_id'],
      'reward_name' : args['reward_name'],
      'user_id' : user['id']
    }

    history = RewardHistories(new_history)
    db.session.add(history)
    db.session.commit()

    app.logger.debug('DEBUG : %s', history)

    return marshal(history, RewardHistories.response_fields), 200, {'Content_Type': 'application/json'}
  

api.add_resource(UserRewardHistoriesResource, '/user')
api.add_resource(AdminRewardHistoriesResource, '')
