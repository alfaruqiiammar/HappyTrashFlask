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
    """User with id 100 has not been created, hence will get a 404 respond"""

    token = createTokenAdmin()
    res = client.get('/v1/users/admin/100', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 404

  ####### User get a single user

  def testGetOneByUser(self,client):
    token = createTokenUser()
    res = client.get('/v1/users/1', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 200

  def testGetOneByUserInvalid(self,client):
    """User in createTokenUser is user with id 1, hence will not be able to access user 2 profile"""

    token = createTokenUser()
    res = client.get('/v1/users/2', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 403

  def testGetOneUserNotFound(self,client):
    """User with id 100 has not been created, hence will get a 404 respond"""

    token = createTokenUser()
    res = client.get('/v1/users/100', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 404
  
  ##### admin get all user data

  def testGetAll(self, client):
    token = createTokenAdmin()
    res = client.get('/v1/users/all', headers = {'Authorization' : 'Bearer ' + token})
    assert res.status_code == 200

  def testGetAllByUser(self, client):
    """Only admin can see data from all users, hence request will gwt 403 respond"""

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
  
  def testAttrributeOptions(self, client):
    res = client.options('/v1/user_attributes')
    assert res.status_code == 200
  
  ##### Put user profile

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
    """Missing .domain in email"""

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
    """Missing 0 at the beginning of phone number"""

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
    """User try to input the same email as he/she has
    check in put test with status 200
    """

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

  def testUserPutEmailAlreadyListed2(self, client):
    """User try to input the same email as admin
    check in __init__.py function createDatabase
    """

    token = createTokenUser()
    data = {
       "email": "admin@admin.com"
       }
    res=client.put('/v1/users', 
                     data=json.dumps(data),
                     headers = {'Authorization' : 'Bearer '+token},
                     content_type='application/json')

    res_json=json.loads(res.data)

    assert res.status_code == 400
 
  def testUserPutMobileNumberAlreadyListed(self, client):
    """User try to input the same phone number as he/she has
    check in put test with status 200
    """
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

  ###### Put user onboarding status
 
  def testPutAttribute(self, client):
    token = createTokenUser()
    res = client.put('/v1/user_attributes',
                      headers = {'Authorization' : 'Bearer '+token}
                      )
    assert res.status_code == 200
  
  def testPutAttributeMissingHeader(self, client):
    token = createTokenUser()
    res = client.put('/v1/user_attributes')
    assert res.status_code == 401