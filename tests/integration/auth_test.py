import json
from tests import app, client, cache
from tests import reset_database

class TestAuth():

    reset_database()

######### options
    def testAuthOption(self, client):
        res = client.options('/v1/users')
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

    # def testUserRegisterInvalidEmail(self, client):
    #     data = {
    #         "name": "dadang",
    #         "email": "dadang@conello",
    #         "mobile_number": "08121212123",
    #         "password": "dadangajah"
    #     }
    #     res=client.post('/v1/users', 
    #                     data=json.dumps(data),
    #                     content_type='application/json')

    #     res_json=json.loads(res.data)

    #     assert res.status_code == 400

    # def testUserRegisterInvalidMobileNumber(self, client):
    #     data = {
    #         "name": "dadang",
    #         "email": "dadang2@conello.com",
    #         "mobile_number": "812121212",
    #         "password": "dadangajah"
    #     }
    #     res=client.post('/v1/users', 
    #                     data=json.dumps(data),
    #                     content_type='application/json')

    #     res_json=json.loads(res.data)

    #     assert res.status_code == 400

    # def testUserRegisterEmailAlreadyListed(self, client):
    #     data = {
    #         "name": "dadang",
    #         "email": "dadang@conello.com",
    #         "mobile_number": "08121212123",
    #         "password": "dadangajah"
    #     }
    #     res=client.post('/v1/users', 
    #                     data=json.dumps(data),
    #                     content_type='application/json')

    #     res_json=json.loads(res.data)

    #     assert res.status_code == 400

    # def testUserRegisterMobileNumberAlreadyListed(self, client):
    #     data = {
    #         "name": "dadang",
    #         "email": "dadang2@conello.com",
    #         "mobile_number": "0812121212",
    #         "password": "dadangajah"
    #     }
    #     res=client.post('/v1/users', 
    #                     data=json.dumps(data),
    #                     content_type='application/json')

    #     res_json=json.loads(res.data)

    #     assert res.status_code == 400


