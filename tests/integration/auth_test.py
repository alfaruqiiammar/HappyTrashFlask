import json
from tests import app, client, cache, resetDatabase, createTokenUser

class TestAuth():

    resetDatabase()

######### options
    def testAuthOption(self, client):
        res = client.options('/v1/auth')
        assert res.status_code == 200

######### post

    def testLogin(self, client):
        data = {
            "email": "user@user.com",
            "password": "user"
        }
        res=client.post('/v1/auth', 
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 200

    def testLoginInvalidEmailFormat(self, client):
        data = {
            "email": "user@user",
            "password": "user"
        }
        res=client.post('/v1/auth', 
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 400

    def testLoginInvalidEmail(self, client):
        data = {
            "email": "user@user.co",
            "password": "user"
        }
        res=client.post('/v1/auth', 
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 401

    def testLoginInvalidPassword(self, client):
        data = {
            "email": "user@user.com",
            "password": "userbad"
        }
        res=client.post('/v1/auth', 
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 401


######### get
    def testGetUserInformation(self, client):
        token = createTokenUser()
        res = client.get('/v1/auth',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200




