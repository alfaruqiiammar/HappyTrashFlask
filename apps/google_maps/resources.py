from flask import Blueprint
from flask_restful import Resource, reqparse, Api
import requests, json
from flask_jwt_extended import jwt_required
from apps import userRequired

bp_google_maps = Blueprint('google_maps', __name__)
api = Api(bp_google_maps)

class GoogleMapsResources(Resource):
    """Class for storing HTTP request method access Google Maps API"""

    def __init__(self):
        """Init function needed to indicate this is a class, but never used"""
        pass

    def options(self):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return {'Status': 'OK'}, 200

    ## Function for get address by latitude and longitude inputted by user
    @jwt_required
    @userRequired
    def get(self):
        """Get address by latitude and longitude inputted by user

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "claims": {
                    "id": 1,
                    "email": "dadang@conello.com",
                    "mobile_number": "0812121212121",
                    "role": False
                }
            }
        """

        parser = reqparse.RequestParser()
        parser.add_argument('lat', location='args', default=None)
        parser.add_argument('lng', location='args', default=None)
        args = parser.parse_args()

        google_maps_host = 'https://maps.googleapis.com/maps/api/geocode/json'
        google_maps_api_key = 'AIzaSyAtJjcjFBzjxF908drCFRGAXBF-EvefsSo'

        params = "?latlng={},{}&key={}".format(args['lat'], args['lng'], google_maps_api_key)

        url = "{host}{params}".format(host=google_maps_host, params=params)

        latlng = "{lat},{lng}".format(lat=args['lat'], lng=args['lng'])

        request = requests.get(google_maps_host, params={'latlng': latlng, 'key': google_maps_api_key})
        address = request.json()['results'][0]['formatted_address']
        response = {
            "adress": address
        }

        return response, 200, {'Content-Type': 'application/json'}
        

api.add_resource(GoogleMapsResources, '')
