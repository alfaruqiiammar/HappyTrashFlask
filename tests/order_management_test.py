import json
from . import app, client, cache, resetDatabase, createTokenAdmin, createTokenUser

class TestOrderManagement():
  resetDatabase()
  temp_order_id = None
  def testOrderPost(self, client):
    token = createTokenUser()
    order = {
      "adress" : "args",
      "time" : "2018-03-29T13:34:00.000",
      "photo" : "args"
      }
    res = client.post('/v1/orders', data = json.dumps(order), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json' )

    res_json = json.loads(res.data)
    TestOrderManagement.temp_order_id = res_json['id']
    assert res.status_code == 200

  def testOrderPostInvalidAdress(self, client):    
    token = createTokenUser()
    order = {
      "photo" : "args"
      }
    res = client.post('/v1/orders', data = json.dumps(order), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json' )

    res_json = json.loads(res.data)
    assert res.status_code == 400

  def testOrderPostInvalidUser(self, client):
    token = createTokenAdmin()
    order = {
      "adress" : "args",
      "time" : "2018-03-29T13:34:00.000",
      "photo" : "args"
      }
    res = client.post('/v1/orders', data = json.dumps(order), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json' )

    res_json = json.loads(res.data)
    assert res.status_code == 403

  def testOrderPutCancelled(self,client):
    token = createTokenUser()
    order_status = {
      "status" : "cancelled"
    }

    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')

    assert res.status_code == 200

  def testOrderPutInvalidStatus(self,client):
    token = createTokenUser()
    order_status = {
      "status" : "cancelledmaybe"
    }

    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    
    assert res.status_code == 400
  
  def testOrderPutCancelledByAdmin(self,client):
    token = createTokenAdmin()
    order_status = {
      "status" : "cancelled"
    }
    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 403
  
  def testPutRejected(self,client):
    token = createTokenAdmin()
    order_status = {
      "status" : "rejected"
    }
    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 200
  
  def testPutRejectedByUser(self,client):
    token = createTokenUser()
    order_status = {
      "status" : "rejected"
    }
    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 403

  def testPutConfirmed(self,client):
    token = createTokenAdmin()
    order_status = {
      "status" : "confirmed"
    }
    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 200
  
  def testPutConfirmedByUser(self,client):
    token = createTokenUser()
    order_status = {
      "status" : "confirmed"
    }
    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    assert res.status_code == 403


  def testOrderPutNotFound(self,client):
    token = createTokenUser()
    order_status = {
      "status" : "cancelled"
    }
    
    res = client.put('/v1/orders/123456787', data = json.dumps(order_status),headers = {'Authorization' : "Bearer " + token}, content_type = 'application/json')
    
    assert res.status_code == 404

  def testOrderPutDone(self, client):
    token = createTokenAdmin()
    order_status = {
      "status" : "done",
      "details" : [
		        {"trash_id": 1,
			      "qty" : 2.9
		        },
		        {"trash_id": 2,
			      "qty" : 1.2
	          }
			      ]
    }

    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    
    assert res.status_code == 200  

  def testOrderPutDoneByUser(self, client):
    token = createTokenUser()
    order_status = {
      "status" : "done",
      "details" : [
		        {"trash_id": 1,
			      "qty" : 2.9
		        },
		        {"trash_id": 2,
			      "qty" : 1.2
	          }
			      ]
    }

    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status), headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 403    
  
  def testOrderGet(self,client):
    token = createTokenAdmin()

    res = client.get('/v1/orders',headers = {'Authorization' : "Bearer " + token},content_type = 'application/json')
    assert res.status_code == 200

  def testOrderOptions(self, client):
    res = client.options('/v1/orders')
    assert res.status_code == 200
  
  def testUserOrderOptions(self, client):
    res = client.options('/v1/orders/user')
    assert res.status_code == 200
  
  def testUserOrderGet(self, client):
    token = createTokenUser()
    res = client.get('v1/orders/user', headers={'Authorization' : "Bearer " + token}, content_type='application/json')

    assert res.status_code == 200

  def testUserOrderGetInvalidToken(self, client):
    token = createTokenAdmin()
    res = client.get('v1/orders/user', headers={'Authorization' : "Bearer " + token}, content_type='application/json')

    assert res.status_code == 403