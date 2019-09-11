import json
from tests import app, client, cache
from tests import reset_database

class TestUsersRegister():

    reset_database()

######### post

    def test_user_register(self, client):
        data = {
            "name": "dadang",
            "email": "dadang@conello.com",
            "mobile_number": "0812121212",
            "password": "dadangajah"
        }
        res=client.post('/v1/users', 
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 200


