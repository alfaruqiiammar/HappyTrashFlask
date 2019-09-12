import json
from . import app, client, cache, createTokenAdmin, createTokenUser

class TestRewardHistories():
  temp_history_id = None
  

  def testHistoryPost(self,client):