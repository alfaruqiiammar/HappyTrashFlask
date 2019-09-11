import json
from . import app, client, cache

class TestTrashCategoriesCrud():
  temp_id = None

  def testTrashCategoriesPost(self, client):
    category = {
      "category_name" : "dummy_name"
    }
    res = client.post('/trash_category', data = json.dumps(category), content_type = 'application/json' )

    res_json = json.loads(res.data)
    TestTrashCategoriesCrud.temp_id = res_json['id']
    assert res.status_code == 200
  
  def testTrashCategoriesGet(self, client):
    res = client.get('/trash_category', content_type = 'application/json')
    assert res.status_code == 200
  
  