import json
from tests import app, client, cache, resetDatabase
from mock import patch
from apps.google_maps.resources import GoogleMapsResources
from tests import client


class TestGoogleApi():
    """class for testing google maps api"""

    def testGoogleMapOptions(self, client):
        """test options function in GoogleMapResources"""

        res = client.options('/v1/google_maps')
        assert res.status_code == 200

    @patch.object(GoogleMapsResources, 'get')
    def testGoogleMapApi(self, mock_get, client):
        """tests get function in GoogleMapsResource using mock up"""

        temp = {"adress": "Jl. Tidar No. 23, Sukun, Malang"}
        mock_get.return_value = temp
        data = {
            'lat': '1.23456',
            'lng': '-2.0998327'
        }
        res = client.get('/v1/google_maps', query_string=data,
                         content_type='application/json')
        assert json.loads(res.data) == temp
