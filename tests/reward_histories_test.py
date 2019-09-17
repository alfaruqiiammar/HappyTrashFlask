import json
from . import app, client, cache, createTokenAdmin, createTokenUser, resetDatabase


class TestRewardHistories():
    """Class for testing function that directly related to reward histories table"""

    resetDatabase()
    temp_history_id = None

    def testHistoryPost(self, client):
        """Test posting a new record to reward history table"""

        token = createTokenUser()
        history = {
            "reward_id": 1,
            "reward_name": "dummy_reward"
        }
        res = client.post('/v1/reward_history/user', data=json.dumps(history), headers={
                          'Authorization': "Bearer " + token}, content_type='application/json')
        res_json = json.loads(res.data)
        TestRewardHistories.temp_history_id = res_json['id']
        assert res.status_code == 200

    def testHistoryGetByAdmin(self, client):
        """test get all data from reward history by admin"""
        token = createTokenAdmin()
        res = client.get('/v1/reward_history', headers={
                         'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testHistoryGetByUser(self, client):
        """test get all data from reward history by user"""
        token = createTokenUser()
        res = client.get('/v1/reward_history/user', headers={
                         'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testOptionsRewardHistories(self, client):
        """test options function at /reward_history endpoint"""
        res = client.options('/v1/reward_history')
        assert res.status_code == 200

    def testOptionsRewardHistories2(self, client):
        """test options function at /reward_history/user endpoint"""
        res = client.options('/v1/reward_history/user')
        assert res.status_code == 200
