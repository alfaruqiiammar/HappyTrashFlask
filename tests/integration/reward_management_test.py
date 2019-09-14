import json
from tests import app, client, cache, resetDatabase, createTokenAdmin


class TestRewardManagement():

    resetDatabase()

# options
    def testRewardOption(self, client):
        res = client.options('/v1/rewards/1')
        assert res.status_code == 200

# post

    def testInputReward(self, client):
        token = createTokenAdmin()
        data = {
            "name": "tes2",
            "point_to_claim": 1,
            "photo": "tes",
            "stock": 1,
            "status": True
        }
        res = client.post('/v1/rewards',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 200

# get
    def testGetAllRewards(self, client):
        token = createTokenAdmin()
        res = client.get('/v1/rewards',
                         headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

# put

    def testEditReward(self, client):
        token = createTokenAdmin()
        data = {
            "name": "tes2",
            "point_to_claim": 1,
            "photo": "tes",
            "stock": 1,
            "status": False
        }
        res = client.put('/v1/rewards/1',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def testEditRewardInvalidId(self, client):
        token = createTokenAdmin()
        data = {
            "name": "tes2",
            "point_to_claim": 1,
            "photo": "tes",
            "stock": 1,
            "status": False
        }
        res = client.put('/v1/rewards/3',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 404
