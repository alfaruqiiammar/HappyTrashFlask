import json
from tests import app, client, cache, resetDatabase, createTokenAdmin, createTokenUser


class TestRewardManagement():
    """Class for testing all functions that are directly related to rewards table"""
    resetDatabase()

# options
    def testRewardOption(self, client):
        """test options function for /rewards endpoint"""
        res = client.options('/v1/rewards/3')
        assert res.status_code == 200

# post

    def testInputReward(self, client):
        """test put a record in rewards table with valid token and data"""
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
        """test get all rewards data from rewards table using valid token"""
        token = createTokenAdmin()
        res = client.get('/v1/rewards',
                         headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

# put

    def testEditReward(self, client):
        """test put a record in rewards table using admin token"""
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

        assert res.status_code == 200

    def testEditRewardUser(self, client):
        """test put a record in rewards table using user token"""
        token = createTokenUser()
        data = {
            "stock": 1
        }
        res = client.put('/v1/rewards/3',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def testEditRewardInvalidId(self, client):
        """test put a reward record which id is not in the table,
        hence will raise 404(Not Found) error"""
        token = createTokenAdmin()
        data = {
            "name": "tes2",
            "point_to_claim": 1,
            "photo": "tes",
            "stock": 1,
            "status": False
        }
        res = client.put('/v1/rewards/23',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 404
