import json
from . import app, client, cache

class TestOrderManagement():
  temp_order_id = None
  def testOrderPost(self, client):
    order = {
      "adress" : "args",
      "time" : "2018-03-29T13:34:00.000",
      "photo" : "args"
      }
    res = client.post('/v1/orders', data = json.dumps(order), content_type = 'application/json' )

    res_json = json.loads(res.data)
    TestOrderManagement.temp_order_id = res_json['id']
    assert res.status_code == 200

  def testOrderPostInvalidAdress(self, client):    
    order = {
      "photo" : "args"
      }
    res = client.post('/v1/orders', data = json.dumps(order), content_type = 'application/json' )

    res_json = json.loads(res.data)
    assert res.status_code == 400
  
  def testOrderPutCancelled(self,client):
    order_status = {
      "status" : "cancelled"
    }

    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status), content_type = 'application/json')
    assert res.status_code == 200
  
  def testOrderPutNotFound(self,client):
    order_status = {
      "status" : "cancelled"
    }

    res = client.put('/v1/orders/12345678'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status), content_type = 'application/json')
    assert res.status_code == 404

  def testOrderPutDone(self, client):
    order_status = {
      "status" : "done",
      "details" : [
		        {"trash_id": 8,
			      "qty" : 2.9
		        },
		        {"trash_id": 9,
			      "qty" : 1.2
	          }
			      ]
    }

    res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data = json.dumps(order_status), content_type = 'application/json')
    assert res.status_code == 200    
  
  def testOrderGet(self,client):
    res = client.get('/v1/orders',content_type = 'application/json')
    assert res.status_code == 200

  def testOrderOptions(self, client):
    res = client.options('/v1/orders')
    assert res.status_code == 200
  
  def testUserOrderOptions(self, client):
    res = client.options('/v1/orders/user')
    assert res.status_code == 200
  
  # def testUserOrderGet(self, client):
    # token = createTokenUser()
    # # res = client.get('v1/orders/user', headers={'Authorization' : "Bearer " + token}, content_type='application/json')
# 
    # assert res.status_code == 200
# 
  # def testUserOrderGetInvalidToken(self, client):
    # token = createTokenAdmin()
    # # res = client.get('v1/orders/user', headers={'Authorization' : "Bearer " + token}, content_type='application/json')
# 
    # assert res.status_code == 403