import logging

from flask import request
from flask_restplus import Resource, reqparse
from rest_api_oscar.api.oscar.business import create_station, delete_station, update_station, get_all_stations, get_station, search_stations
from rest_api_oscar.api.oscar.serializers import station, station_search
from rest_api_oscar.api.restplus import api
import rest_api_oscar.api.oscar.utils as tokenutils
import os, json

log = logging.getLogger(__name__)

ns = api.namespace('stations', description='Operations related to OSCAR stations ')

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1)
pagination_arguments.add_argument('per_page', type=int, required=False,
                                  choices=[5, 10, 20, 30, 40, 50], default=10)


search_params = [ 
    [ 'facilityType' , str , False ] , 
    [ 'stationClass' , str , False ] , 
    [ 'programAffiliation' , str , False ] ,
    [ 'wmoRegion' , str , False ] ,
    [ 'territoryName' , str , False ], 
    [ 'programAffiliation' , str , False ],
    [ 'climateZone' , str , False ],
]                                  
                                  
search_arguments = reqparse.RequestParser()

for param in search_params:
    choices = tokenutils.read_codelist( param[0] )
    search_arguments.add_argument( param[0], type=param[1] , required=param[2] , choices =  choices , help = "{} from WMO codelist repo".format(param[0])  )

search_arguments.add_argument('organization', type=str, required=False)
search_arguments.add_argument('variable', type=int, required=False)
search_arguments.add_argument('latitudeMin', type=float, required=False)
search_arguments.add_argument('latitudeMax', type=float, required=False)
search_arguments.add_argument('longitudeMin', type=float, required=False)
search_arguments.add_argument('longitudeMax', type=float, required=False)
search_arguments.add_argument('elevationMin', type=int, required=False)
search_arguments.add_argument('elevationMax', type=int, required=False)

                                  
@ns.route('/search')
class StationSearch(Resource):
            
    @api.expect(search_arguments,validate=True)
    @api.marshal_list_with(station_search)
    def get(self):
        """
        Returns a list of stations matching the search parameters
        """
        params = request.args
        
        return search_stations(params)
                                  
                                  
@ns.route('/')
class StationCollection(Resource):

    @api.marshal_list_with(station,skip_none=True)
    @api.expect(pagination_arguments,validate=True)
    def get(self):
        """
        Returns list of oscar stations.
        """
        nr_stations = int(request.args.get("per_page",default=10))
        page_nr = int(request.args.get("page",default=1))
        return get_all_stations(page_nr,nr_stations)

    @api.response(201, 'Station successfully created')
    @api.response(400, 'Validation error')
    @api.response(401, 'Authentication problem')
    @api.response(500, 'Processing error')
    @api.doc(security='apikey')    
    @api.expect(station)
    def post(self):
        """Creates a new oscar station."""
        
        token = request.headers.get(tokenutils.OSCAR_TOKEN) 
        station_data = request.json

        if not token:
            return "auth header not set", 401

        [cookies,qlack_token] = tokenutils.decode_token(token)

        # mock_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../../tmp/new-station.json'))        
        # with open(mock_file) as f:
            # mock_station_data = json.load(f)
            # mock_station_data["wigosIds"][0]["wid"] = station_data["wigosIds"][0]["wid"]
            # mock_station_data["name"] = station_data["name"]
        
        # station_data = mock_station_data

        
        [status_code,info] = create_station(station_data,cookies,qlack_token) 
        if status_code == 200:
            return { "station_id" : info } , 201
        if status_code == 400:
            return info, 400   
        else:
            return None, 500


@ns.route('/<int:id>')
@api.response(404, 'Station not found.')
class StationItem(Resource):

    @api.marshal_with(station,skip_none=True)
    def get(self, id):
        """Returns details of a station."""
        return get_station(id)

    @api.expect(station)
    @api.response(204, 'Station successfully updated.')
    @api.response(401, 'Authentication problem')
    @api.response(404, 'Station not found.')
    @api.response(500, 'Porcessing error')
    @api.doc(security='apikey')    
    def put(self, id):
        """Updates a station."""
        
        token = request.headers.get(tokenutils.OSCAR_TOKEN) 
        station_data = request.json
        
        mock_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../../tmp/station.json'))
        with open(mock_file) as f:
            mock_station_data = json.load(f)
            mock_station_data["descriptions"][0]["description"] += station_data["descriptions"][0]["description"]
        
        station_data = mock_station_data
        
        if not token:
            return "auth header not set", 401
            
        [cookies,qlack_token] = tokenutils.decode_token(token)
        ret = update_station(id, station_data,cookies,qlack_token)
        
        if ret:
            return None, 204
        else:
            return None, 500

    @api.response(204, 'Station successfully deleted.')
    @api.doc(security='apikey')    
    def delete(self, id):
        """Deletes station """
        delete_station(id)
        return None, 204
