import json
from . import app, client, cache, createTokenAdmin, createTokenUser, resetDatabase

class TestRewardHistories():

  resetDatabase()
  temp_history_id = None

  def testHistoryPost(self,client):
    """Test posting a new record to reward history table"""

    token = createTokenUser()
    history = {
      "reward_id" : 1,
      "reward_name" : "deletelater"
    }

    res = client.post('/v1/reward_history/user', data = json.dumps(history),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json' )

    res_json = json.loads(res.data)
    TestRewardHistories.temp_history_id = res_json['id']
    assert res.status_code == 200
  
  def testHistoryGetByAdmin(self, client):
    """test get all data from reward history by admin"""
    
    token = createTokenAdmin()
    res = client.get('/v1/reward_history', headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 200


  def testHistoryGetByUser(self, client):
    """test get all data from reward history by admin"""
    token = createTokenUser()
    res = client.get('/v1/reward_history/user', headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 200