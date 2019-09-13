import json
from tests import app, client, cache, resetDatabase, createTokenAdmin, createTokenUser

class TestUserProfile():

  resetDatabase()

  ######options

  def testOptionsAdmin(self, client):
    res = client.options('/v1/users/admin')
    assert res.status_code == 200

  ###### admin get single user

  def testGetOneByAdmin(self,client):

    token = createTokenAdmin()
    res = client.get('/v1/users/admin/2', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 200
  
  def testGetOneByAdminNotFound(self,client):

    token = createTokenAdmin()
    res = client.get('/v1/users/admin/100', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 404

  ####### User get a single user

  def testGetOneByUser(self,client):
    token = createTokenUser()
    res = client.get('/v1/users/1', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 200

  def testGetOneByUserInvalid(self,client):
    token = createTokenUser()
    res = client.get('/v1/users/2', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 403

  def testGetOneUserNotFound(self,client):
    token = createTokenUser()
    res = client.get('/v1/users/100', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 404
  
  ##### admin get all user data

  def testGetAll(self, client):
    token = createTokenAdmin()
    res = client.get('/v1/users/all', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 200

  def testGetAllByUser(self, client):
    token = createTokenUser()
    res = client.get('/v1/users/all', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 403

  ###### options

  def testAdminOptions(self,client):
    res = client.options('/v1/users/admin')
    assert res.status_code == 200

  def testAdminAllOptions(self,client):
    res = client.options('/v1/users/all')
    assert res.status_code == 200
  
  ##### Put

  def testUserPut(self, client):
    token = createTokenUser()
    data = {
      "name": "dadang",
      "email": "put@conello.com",
      "mobile_number": "08812121212",
      "password": "dadangajah"
      }
    res=client.put('/v1/users', 
                    data=json.dumps(data),
                    headers = {'Authorization' : 'Bearer '+token},
                    content_type='application/json')

    res_json=json.loads(res.data)

    assert res.status_code == 200

  def testUserPutInvalidEmail(self, client):
    token = createTokenUser()
    data = {
        "email": "dadang@conello",
    }
    res=client.put('/v1/users', 
                    data=json.dumps(data),
                    headers = {'Authorization' : 'Bearer '+token},
                    content_type='application/json')
    res_json=json.loads(res.data)
    assert res.status_code == 400

  def testUserPutInvalidMobileNumber(self, client):
    token = createTokenUser()
    data = {
        "mobile_number": "812121212"
    }
    res=client.put('/v1/users', 
                    data=json.dumps(data),
                    headers = {'Authorization' : 'Bearer '+token},
                    content_type='application/json')
    res_json=json.loads(res.data)
    assert res.status_code == 400
 
  def testUserPutEmailAlreadyListed(self, client):
    token = createTokenUser()
    data = {
       "email": "put@conello.com"
       }
    res=client.put('/v1/users', 
                     data=json.dumps(data),
                     headers = {'Authorization' : 'Bearer '+token},
                     content_type='application/json')

    res_json=json.loads(res.data)

    assert res.status_code == 400
 
  def testUserPutMobileNumberAlreadyListed(self, client):
    token = createTokenUser()
    data = {
        "mobile_number": "08812121212"
    }
    res=client.put('/v1/users', 
                    data=json.dumps(data),
                    headers = {'Authorization' : 'Bearer '+token},
                    content_type='application/json')
    res_json=json.loads(res.data)
    assert res.status_code == 400