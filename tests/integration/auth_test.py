import json
from tests import app, client, cache, resetDatabase, createTokenUser


class TestAuth():
    """Class for testing all functions that are directly related to user's authentification"""

    resetDatabase()

#### options ####
    def testAuthOption(self, client):
        """test options function for /auth endpoint"""
        res = client.options('/v1/auth')
        assert res.status_code == 200

    def testAuthOption2(self, client):
        """test options function for /auth/refresh endpoint"""
        res = client.options('/v1/auth/refresh')
        assert res.status_code == 200

#### post ####

    def testLogin(self, client):
        """test user login"""
        data = {
            "email": "user@user.com",
            "password": "user"
        }
        res = client.post('/v1/auth',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def testLoginInvalidEmailFormat(self, client):
        """test user login with invalid credentials format, hence will raise 400(bad request) error"""
        data = {
            "email": "user@user",
            "password": "user"
        }
        res = client.post('/v1/auth',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 400

    def testLoginInvalidEmail(self, client):
        """test user login with invalid credentials(not found in database), hence will raise 401(unauthorized) error"""
        data = {
            "email": "user@user.co",
            "password": "user"
        }
        res = client.post('/v1/auth',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 401

    def testLoginInvalidPassword(self, client):
        """test user login with invalid credentials(not found in database), hence will raise 401(unauthorized) error"""
        data = {
            "email": "user@user.com",
            "password": "userbad"
        }
        res = client.post('/v1/auth',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 401

    def testGetUserInformation(self, client):
        """test get user's jwt claims"""
        token = createTokenUser()
        res = client.get('/v1/auth',
                         headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

#### refresh ####
    def testRefreshToken(self, client):
        """ test refreshing user's token"""
        token = createTokenUser()
        res = client.post('/v1/auth/refresh',
                          headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
