from apps import db
from flask_restful import fields
import datetime


class RewardHistories(db.Model):
  """Class for storing information about reward that users have got

    Attributes:
        __tablename__: a string of table name
        reward_id: an integer of reward's id
        reward_name :the alias of the reward
        user_id : an integer of user's id
        created_at: a datetime that indicates when the user got the reward
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
  __tablename__ = "reward_histories"

  id = db.Column(db.Integer, primary_key = True)
  reward_id = db.Column(db.Integer, nullable = False)
  reward_name = db.Column(db.String(100), nullable = False)
  user_id = db.Column(db.Integer, nullable = False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  response_fields = {
        'id': fields.Integer,
        'reward_id': fields.Integer,
        'reward_name' : fields.String,
        'user_id' : fields.Integer,
        'created_at': fields.DateTime
    }

  def __init__(self, data):
    self.reward_id = data.reward_id
    self.reward_name = data.reward_name
    self.user_id = data.user_id
      