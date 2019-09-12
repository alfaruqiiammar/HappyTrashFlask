import json
from . import app, client, cache, createTokenAdmin, createTokenUser

class TestTrashManagement():
  temp_category_id = None
  temp_trash_id = None

  def testTrashCategoriesPost(self, client):
    token = createTokenAdmin()
    category = {
      "category_name" : "dummy_name"
    }
    res = client.post('/v1/trash_category', data = json.dumps(category),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json' )

    res_json = json.loads(res.data)
    TestTrashManagement.temp_category_id = res_json['id']
    assert res.status_code == 200
  
  def testTrashCategoriesGetByAdmin(self, client):
    token = createTokenAdmin()
    res = client.get('/v1/trash_category', headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 200

  def testTrashCategoriesGetByUser(self, client):
    token = createTokenUser()
    res = client.get('/v1/trash_category', headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 200

  def testTrashCategoriesPut(self, client):
    token = createTokenAdmin()
    new_name = {
      "category_name" : "newdummy"
    }

    res = client.put('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id), data = json.dumps(new_name),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 200

  def testTrashCategoriesPutInvalidAdmin(self, client):
    token = createTokenUser()
    new_name = {
      "category_name" : "newdummy"
    }

    res = client.put('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id), data = json.dumps(new_name),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 403
  
  def testTrashCategoriesPutInvalidName(self, client):
    token = createTokenAdmin()
    new_name = {
      "category_name" : None
    }

    res = client.put('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id), data = json.dumps(new_name),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 400
  
  def testTrashCategoriesPutInvalidId(self, client):
    token = createTokenAdmin()
    new_name = {
      "category_name" : "dummyname"
    }
    res = client.put('/v1/trash_category/none', data = json.dumps(new_name),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 404

#######
  def testTrashPost(self, client):
    token = createTokenAdmin()
    trash = {
      "trash_category_id" : TestTrashManagement.temp_category_id,
      "trash_name" : "test",
      "photo" : "test",
      "price" : 100,
      "point" : 1
    }
    res = client.post('/v1/trash', data = json.dumps(trash),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json' )

    res_json = json.loads(res.data)
    TestTrashManagement.temp_trash_id = res_json['id']
    assert res.status_code == 200
  
  def testTrashGet(self, client):
    token = createTokenAdmin()
    res = client.get('/v1/trash',headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 200
  
  def testTrashPut(self, client):
    token = createTokenAdmin()
    new_details = {
      "trash_category_id" : 1,
      "trash_name" : "test",
      "photo" : "test",
      "price" : 100,
      "point" : 1
    }

    res = client.put('/v1/trash/{}'.format(TestTrashManagement.temp_trash_id), data = json.dumps(new_details),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 200
  
  def testTrashPutByUser(self, client):
    token = createTokenUser()
    new_details = {
      "trash_category_id" : 1,
      "trash_name" : "test",
      "photo" : "test",
      "price" : 100,
      "point" : 1
    }

    res = client.put('/v1/trash/{}'.format(TestTrashManagement.temp_trash_id), data = json.dumps(new_details),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 403
  
  def testTrashPutInvalidId(self, client):
    token = createTokenAdmin()
    new_details = {
      "trash_name" : "test",
      "photo" : "test",
      "price" : 100,
      "point" : 1
    }
    res = client.put('/v1/trash/none', data = json.dumps(new_details), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 404

  def testTrashDelete(self, client):
    token = createTokenAdmin()
    res = client.delete('/v1/trash/{}'.format(TestTrashManagement.temp_trash_id), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 200 

  def testTrashDeleteInvalidId(self, client):
    token = createTokenAdmin()
    res = client.delete('/v1/trash/{}'.format(TestTrashManagement.temp_trash_id), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 404
#######

  def testTrashCategoriesDelete(self, client):
    token = createTokenAdmin()
    res = client.delete('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 200 

  def testTrashCategoriesDeleteInvalidId(self, client):
    token = createTokenAdmin()
    res = client.delete('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 404   
  
  def testOptionsTrash(self, client):
    res = client.options('/v1/trash')
    assert res.status_code == 200

  def testOptionsTrashCategories(self, client):
    res = client.options('/v1/trash_category')
    assert res.status_code == 200