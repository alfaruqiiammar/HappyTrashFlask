import json
from . import app, client, cache, resetDatabase, createTokenAdmin, createTokenUser


class TestOrderManagement():
    """Class for testing all function that directly related to order table"""

    resetDatabase()
    temp_order_id = None

    #### post ####
    def testOrderPost(self, client):
        """test posting a new order to table with valid data an header"""
        token = createTokenUser()
        order = {
            "adress": "args",
            "time": "2018-03-29T13:34:00.000",
            "photo": "args"
        }
        res = client.post('/v1/orders', data=json.dumps(order), headers={
                          'Authorization': "Bearer " + token}, content_type='application/json')

        res_json = json.loads(res.data)
        TestOrderManagement.temp_order_id = res_json['id']
        assert res.status_code == 200

    def testOrderPostInvalidAdress(self, client):
        """test posting a new order to table with invalid data (missing address) """

        token = createTokenUser()
        order = {
            "photo": "args"
        }
        res = client.post('/v1/orders', data=json.dumps(order), headers={
                          'Authorization': "Bearer " + token}, content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testOrderPostInvalidUser(self, client):
        """Test posting a new order using admin token. 
        Admin is not permitted to post a new order,hence request will get 403 response
        """

        token = createTokenAdmin()
        order = {
            "adress": "args",
            "time": "2018-03-29T13:34:00.000",
            "photo": "args"
        }
        res = client.post('/v1/orders', data=json.dumps(order), headers={
                          'Authorization': "Bearer " + token}, content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 403

    #### put #####

    def testOrderPutCancelled(self, client):
        """Test put order record with status 'cancelled' using valid token."""
        token = createTokenUser()
        order_status = {
            "status": "cancelled"
        }

        res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data=json.dumps(
            order_status), headers={'Authorization': "Bearer " + token}, content_type='application/json')

        assert res.status_code == 200

    def testOrderPutInvalidStatus(self, client):
        """test put an order record using status 'cancelledmaybe' which is not a valid options for status"""

        token = createTokenUser()
        order_status = {
            "status": "cancelledmaybe"
        }

        res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data=json.dumps(
            order_status), headers={'Authorization': "Bearer " + token}, content_type='application/json')

        assert res.status_code == 400

    def testOrderPutCancelledByAdmin(self, client):
        """Test put an order record using admin's token and status='cancelled'
        Admin permitted to reject, but not permitted to cancel
        hence will raise 403(forbidden) error"""

        token = createTokenAdmin()
        order_status = {
            "status": "cancelled"
        }
        res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data=json.dumps(
            order_status), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 403

    def testPutRejected(self, client):
        """Test put an order record using admin's token and status='rejected'"""

        token = createTokenAdmin()
        order_status = {
            "status": "rejected"
        }
        res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data=json.dumps(
            order_status), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testPutRejectedByUser(self, client):
        """Test put an order record using user's token and status='rejected'
        User permitted to cancel, but not permitted to reject
        hence will raise 403(forbidden) error"""

        token = createTokenUser()
        order_status = {
            "status": "rejected"
        }
        res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data=json.dumps(
            order_status), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 403

    def testPutConfirmed(self, client):
        """Test put an order record using admin's token and status='confirmed'"""
        token = createTokenAdmin()
        order_status = {
            "status": "confirmed"
        }
        res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data=json.dumps(
            order_status), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testPutConfirmedByUser(self, client):
        """Test put an order record using user's token and status='confirmed'
        User is not permitted to change status to confirmed, hence will raise 403(forbidden) error"""
        token = createTokenUser()
        order_status = {
            "status": "confirmed"
        }
        res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data=json.dumps(
            order_status), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 403

    def testOrderPutNotFound(self, client):
        """Test to put an order record with id=123456787, which is not in the table
        hence will raise 404(Not Found) error"""

        token = createTokenUser()
        order_status = {
            "status": "cancelled"
        }

        res = client.put('/v1/orders/123456787', data=json.dumps(order_status), headers={
                         'Authorization': "Bearer " + token}, content_type='application/json')

        assert res.status_code == 404

    def testOrderPutDone(self, client):
        """Test put an order record using admin's token and status='done'"""
        token = createTokenAdmin()
        order_status = {
            "status": "done",
            "details": [
                {"trash_id": 1,
                 "qty": 2.9
                 },
                {"trash_id": 2,
                    "qty": 1.2
                 }
            ]
        }

        res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data=json.dumps(
            order_status), headers={'Authorization': "Bearer " + token}, content_type='application/json')

        assert res.status_code == 200

    def testOrderPutDoneByUser(self, client):
        """Test put an order record using admin's token and status='done'
        User is not permitted to change status to done, hence will raise 403(forbidden) error"""

        token = createTokenUser()
        order_status = {
            "status": "done",
            "details": [
                {"trash_id": 1,
                 "qty": 2.9
                 },
                {"trash_id": 2,
                    "qty": 1.2
                 }
            ]
        }

        res = client.put('/v1/orders/{}'.format(TestOrderManagement.temp_order_id), data=json.dumps(
            order_status), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 403

    #### get ####

    def testOrderGet(self, client):
        """test get all order data from orders table"""

        token = createTokenAdmin()

        res = client.get(
            '/v1/orders', headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testUserOrderGet(self, client):
        """test get all order data for corresponding user from orders table"""

        token = createTokenUser()
        res = client.get(
            'v1/orders/user', headers={'Authorization': "Bearer " + token}, content_type='application/json')

        assert res.status_code == 200

    def testUserOrderGetInvalidToken(self, client):
        """Test get a specific user's order data using admin token,
        hence will raise 403(forbidden) error"""

        token = createTokenAdmin()
        res = client.get(
            'v1/orders/user', headers={'Authorization': "Bearer " + token}, content_type='application/json')

        assert res.status_code == 403

    #### options ####

    def testOrderOptions(self, client):
        """test options function for /orders endpoint"""
        res = client.options('/v1/orders')
        assert res.status_code == 200

    def testUserOrderOptions(self, client):
        """test options function for /orders/user endpoint"""
        res = client.options('/v1/orders/user')
        assert res.status_code == 200
