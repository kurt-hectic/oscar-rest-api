import logging

from flask import request
from flask_restplus import Resource
from rest_api_oscar.api.oscar.business import create_station, delete_station, update_station, get_all_stations, get_station
from rest_api_oscar.api.oscar.serializers import station
from rest_api_oscar.api.restplus import api
#from rest_api_oscar.database.models import Category

log = logging.getLogger(__name__)

ns = api.namespace('stations', description='Operations related to OSCAR stations ')

@ns.route('/')
class StationCollection(Resource):

    @api.marshal_list_with(station)
    def get(self):
        """
        Returns list of oscar stations.
        """
        return get_all_stations()

    @api.response(201, 'Station successfully created.')
    @api.expect(station)
    def post(self):
        """Creates a new oscar station."""
        create_station(request.json)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Station not found.')
class StationItem(Resource):

    @api.marshal_with(station)
    def get(self, id):
        """Returns details of a station."""
        return get_station(id)

    @api.expect(station)
    @api.response(204, 'Station successfully updated.')
    def put(self, id):
        """Updates a station."""
        update_station(id, request.json)
        return None, 204

    @api.response(204, 'Station successfully deleted.')
    def delete(self, id):
        """Deletes station """
        delete_station(id)
        return None, 204
