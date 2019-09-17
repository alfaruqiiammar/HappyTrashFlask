import json
from . import app, client, cache, createTokenAdmin, createTokenUser, resetDatabase


class TestTrashManagement():

    """Class for testing all function that directly related to trash and trash category"""

    resetDatabase()
    temp_category_id = None
    temp_trash_id = None
##############################TRASH CATEGORIES#################

    ##### Post #####

    def testTrashCategoriesPost(self, client):
        """test posting a new trash category to table with valid data an header"""

        token = createTokenAdmin()
        category = {
            "category_name": "dummy_name"
        }
        res = client.post('/v1/trash_category', data=json.dumps(category), headers={
                          'Authorization': "Bearer " + token}, content_type='application/json')

        res_json = json.loads(res.data)
        TestTrashManagement.temp_category_id = res_json['id']
        assert res.status_code == 200

    ##### Get #####
    def testTrashCategoriesGetByAdmin(self, client):
        """Test getting all data from trash category table using token from an admin account"""

        token = createTokenAdmin()
        res = client.get('/v1/trash_category', headers={
                         'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testTrashCategoriesGetByUser(self, client):
        """Test getting all data from trash category table using token from an user account"""

        token = createTokenUser()
        res = client.get('/v1/trash_category', headers={
                         'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    #### Put ####

    def testTrashCategoriesPut(self, client):
        """test put a record in tras category table with valid token and data"""

        token = createTokenAdmin()
        new_name = {
            "category_name": "newdummy"
        }

        res = client.put('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id), data=json.dumps(
            new_name), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testTrashCategoriesPutInvalidAdmin(self, client):
        """test put a record in tras category table with invalid token
        Token used is a non-admin token, hence will raise 403(forbidden) error
        """

        token = createTokenUser()
        new_name = {
            "category_name": "newdummy"
        }

        res = client.put('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id), data=json.dumps(
            new_name), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 403

    def testTrashCategoriesPutInvalidName(self, client):
        """test put a record in trash category table with invalid data.
        category_name is null, hence will raise a 400(bad request) error"""

        token = createTokenAdmin()
        new_name = {
            "category_name": None
        }

        res = client.put('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id), data=json.dumps(
            new_name), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 400

    def testTrashCategoriesPutInvalidId(self, client):
        """test put a record in trash category table with invalid id.
        'none' is an invalid id, hence will raise a 404(Not Found) error"""
        token = createTokenAdmin()
        new_name = {
            "category_name": "dummyname"
        }
        res = client.put('/v1/trash_category/none', data=json.dumps(new_name), headers={
                         'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 404

    ###################################TRASH#####################

    #### Post ####

    def testTrashPost(self, client):
        """test posting a new trash to table with valid data and authorization header"""

        token = createTokenAdmin()
        trash = {
            "trash_category_id": TestTrashManagement.temp_category_id,
            "trash_name": "test",
            "photo": "test",
            "price": 100,
            "point": 1
        }
        res = client.post('/v1/trash', data=json.dumps(trash), headers={
                          'Authorization': "Bearer " + token}, content_type='application/json')

        res_json = json.loads(res.data)
        TestTrashManagement.temp_trash_id = res_json['id']
        assert res.status_code == 200

    #### Get ####

    def testTrashGet(self, client):
        """Test getting all data from trashes table using valid token"""

        token = createTokenAdmin()
        res = client.get(
            '/v1/trash', headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    #### Put ####

    def testTrashPut(self, client):
        """test put a record in tras tableh with valid token and data"""
        token = createTokenAdmin()
        new_details = {
            "trash_category_id": 1,
            "trash_name": "test",
            "photo": "test",
            "price": 100,
            "point": 1
        }

        res = client.put('/v1/trash/{}'.format(TestTrashManagement.temp_trash_id), data=json.dumps(
            new_details), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testTrashPutByUser(self, client):
        """test put a record in trashes table with invalid token
        Token used is a non-admin token, hence will raise 403(forbidden) error
        """

        token = createTokenUser()
        new_details = {
            "trash_category_id": 1,
            "trash_name": "test",
            "photo": "test",
            "price": 100,
            "point": 1
        }

        res = client.put('/v1/trash/{}'.format(TestTrashManagement.temp_trash_id), data=json.dumps(
            new_details), headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 403

    def testTrashPutInvalidId(self, client):
        """test put a record in trashes table with invalid id.
        'none' is an invalid id, hence will raise a 404(Not Found) error"""

        token = createTokenAdmin()
        new_details = {
            "trash_name": "test",
            "photo": "test",
            "price": 100,
            "point": 1
        }
        res = client.put('/v1/trash/none', data=json.dumps(new_details), headers={
                         'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 404

    def testTrashDelete(self, client):
        """Test delete a record in trashes table with valid token"""

        token = createTokenAdmin()
        res = client.delete('/v1/trash/{}'.format(TestTrashManagement.temp_trash_id),
                            headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testTrashDeleteInvalidId(self, client):
        """Test delete a record in trashes table
        trash with id in this test has been deleted in previous test, hence will get a 404(Not Found) error"""
        token = createTokenAdmin()
        res = client.delete('/v1/trash/{}'.format(TestTrashManagement.temp_trash_id),
                            headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 404

################ TRASH CATEGORIES DELETE ############

    def testTrashCategoriesDelete(self, client):
        """Test delete a record in trash category table with valid token and id"""

        token = createTokenAdmin()
        res = client.delete('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id),
                            headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 200

    def testTrashCategoriesDeleteInvalidId(self, client):
        """Test delete a record in trash categories table
        trash with id in this test has been deleted in previous test, hence will get a 404(Not Found) error"""
        token = createTokenAdmin()
        res = client.delete('/v1/trash_category/{}'.format(TestTrashManagement.temp_category_id),
                            headers={'Authorization': "Bearer " + token}, content_type='application/json')
        assert res.status_code == 404

    def testOptionsTrash(self, client):
        """Test options function in resource"""

        res = client.options('/v1/trash')
        assert res.status_code == 200

    def testOptionsTrashCategories(self, client):
        """Test options function in resource"""

        res = client.options('/v1/trash_category')
        assert res.status_code == 200
