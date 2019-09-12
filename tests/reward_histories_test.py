import json
from . import app, client, cache, createTokenAdmin, createTokenUser, resetDatabase

class TestRewardHistories():

  resetDatabase()
  temp_history_id = None

  def testHistoryPost(self,client):
    token = createTokenUser()
    history = {
      "reward_id" : 1,
      "reward_name" : "deletelater"
    }

    res = client.post('/v1/reward_history', data = json.dumps(history),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json' )

    res_json = json.loads(res.data)
    TestRewardHistories.temp_history_id = res_json['id']
    assert res.status_code == 200
