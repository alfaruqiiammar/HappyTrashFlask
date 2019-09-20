import json
from tests import app, client, cache, resetDatabase, createTokenAdmin, createTokenUser


class TestUserProfile():
    """Class for testing all functions that is directly related to users and user attributes"""

    resetDatabase()

    #### options ####

    def testOptionsAdmin(self, client):
        """test options function at /user/admin endpoint"""
        res = client.options('/v1/users/admin')
        assert res.status_code == 200

    #### get ####

    def testGetOneByAdmin(self, client):
        """test get a specific user data using admin token"""

        token = createTokenAdmin()
        res = client.get('/v1/users/admin/2',
                         headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 200

    def testGetOneByAdminNotFound(self, client):
        """test get a specific user data which is not exist in the table using admin token,
        will raise a 404(Not Found) error"""

        token = createTokenAdmin()
        res = client.get('/v1/users/admin/100',
                         headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 404

    def testGetOneByUser(self, client):
        """test get user's data using token"""
        token = createTokenUser()
        res = client.get(
            '/v1/users/1', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 200

    def testGetOneByUserInvalid(self, client):
        """Test get a specific user data, using another user's token.
        User in createTokenUser is user with id 1, hence will not be able to access user 2 profile,
        and raise a 403(forbidden) error"""

        token = createTokenUser()
        res = client.get(
            '/v1/users/2', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 403

    def testGetOneUserNotFound(self, client):
        """Test get a specific user data using another user's token.
        User with id 100 has not been created, hence will get a 404(Not Found) error"""

        token = createTokenUser()
        res = client.get(
            '/v1/users/100', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 404

    def testGetAll(self, client):
        """get all users data from users table"""

        token = createTokenAdmin()
        res = client.get(
            '/v1/users/all', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 200

    def testGetAllByUser(self, client):
        """Test get all users data from users table using user token
        Only admin can see data from all users, hence request will get 403 respond"""

        token = createTokenUser()
        res = client.get(
            '/v1/users/all', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 403

    #### options ####

    def testAdminOptions(self, client):
        """test options function for /users/admin endpoint"""
        res = client.options('/v1/users/admin')
        assert res.status_code == 200

    def testAdminAllOptions(self, client):
        """test options function for /users/all endpoint"""
        res = client.options('/v1/users/all')
        assert res.status_code == 200

    def testAttrributeOptions(self, client):
        """test options function for /user_attributes endpoint"""
        res = client.options('/v1/user_attributes')
        assert res.status_code == 200

    #### Put ####

    def testUserPut(self, client):
        """test put a record in users table with valid data"""
        token = createTokenUser()
        data = {
            "name": "dadang",
            "email": "put@conello.com",
            "mobile_number": "08812121212",
            "password": "dadangajah"
        }
        res = client.put('/v1/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer '+token},
                         content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def testUserPutInvalidEmail(self, client):
        """test put user data to table with invalid email format,
        hence will raise 400(bad request) error"""

        token = createTokenUser()
        data = {
            "email": "dadang@conello",
        }
        res = client.put('/v1/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer '+token},
                         content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPutInvalidMobileNumber(self, client):
        """test put user data to table with invalid mobile number format,
        hence will raise 400(bad request) error"""

        token = createTokenUser()
        data = {
            "mobile_number": "812121212"
        }
        res = client.put('/v1/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer '+token},
                         content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPutOwnerEmail(self, client):
        """test put user data to table with email that is the same with the old email"""

        token = createTokenUser()
        data = {
            "email": "put@conello.com"
        }
        res = client.put('/v1/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer '+token},
                         content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def testUserPutEmailAlreadyListed2(self, client):
        """test put user data to table with mobile number that is already exist in database,
        hence will raise 400(bad request) error"""

        token = createTokenUser()
        data = {
            "email": "admin@admin.com"
        }
        res = client.put('/v1/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer '+token},
                         content_type='application/json')

        res_json = json.loads(res.data)

        assert res.status_code == 400

    def testUserPutMobileNumberAlreadyListed(self, client):
        """put user data to table with mobile number that is already exist in database,
        hence will raise 400(bad request) error"""
        token = createTokenUser()
        data = {
            "mobile_number": "08812121212"
        }
        res = client.put('/v1/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer '+token},
                         content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testPutAttribute(self, client):
        """test put user attributes in user_attributes table"""
        token = createTokenUser()
        res = client.put('/v1/user_attributes',
                         headers={'Authorization': 'Bearer '+token}
                         )
        assert res.status_code == 200

    def testPutAttributeMissingHeader(self, client):
        """test put user attributes in user_attributes table without any token,
        hence will get 401(unauthorized) error"""

        res = client.put('/v1/user_attributes')
        assert res.status_code == 401
