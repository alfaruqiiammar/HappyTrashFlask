import json
from tests import app, client, cache
from tests import resetDatabase


class TestUsersRegister():

    resetDatabase()

#### options ####
    def testUsersOption(self, client):
        """Test options function in user resource file"""
        res = client.options('/v1/users')
        assert res.status_code == 200

#### post ####

    def testUserRegister(self, client):
        """Post a new user data to table"""

        data = {
            "name": "dadang",
            "email": "dadang@conello.com",
            "mobile_number": "0812121212",
            "password": "dadangajah"
        }
        res = client.post('/v1/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def testUserRegisterInvalidEmail(self, client):
        """Post a new user data to table with invalid email format,
        hence will raise 400(bad request) error"""
        data = {
            "name": "dadang",
            "email": "dadang@conello",
            "mobile_number": "08121212123",
            "password": "dadangajah"
        }
        res = client.post('/v1/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 400

    def testUserRegisterInvalidMobileNumber(self, client):
        """Post a new user data to table with invalid mobile number format,
        hence will raise 400(bad request) error"""
        data = {
            "name": "dadang",
            "email": "dadang2@conello.com",
            "mobile_number": "812121212",
            "password": "dadangajah"
        }
        res = client.post('/v1/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 400

    def testUserRegisterEmailAlreadyListed(self, client):
        """Post a new user data to table with email that is already exist in database,
        hence will raise 400(bad request) error"""
        data = {
            "name": "dadang",
            "email": "dadang@conello.com",
            "mobile_number": "08121212123",
            "password": "dadangajah"
        }
        res = client.post('/v1/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 400

    def testUserRegisterMobileNumberAlreadyListed(self, client):
        """Post a new user data to table with mobile number that is already exist in database,
        hence will raise 400(bad request) error"""
        data = {
            "name": "dadang",
            "email": "dadang2@conello.com",
            "mobile_number": "0812121212",
            "password": "dadangajah"
        }
        res = client.post('/v1/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 400
