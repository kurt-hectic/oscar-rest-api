from flask_restplus import fields
from rest_api_oscar.api.restplus import api

program = api.model('Program', {
    "program" : fields.String(required=True,description="program/network")
})

territory = api.model('Territory', {
    "validSince": fields.DateTime(required=True, description="since when"),
    "territoryName": fields.String(required=True, description="name of territory"),
})

timezone = api.model('Time-Zone', {
    "validSince": fields.DateTime(required=True, description="since when"),
    "timezoneName": fields.String(required=True, description="name of territory"),
})

location = api.model('Location', {
    "validSince": fields.DateTime(required=True, description="since when"),
    "latitude": fields.String(required=True, description="latitude"),
    "longitude": fields.String(required=True, description="longitude"),
    "elevation": fields.Integer(required=True, description="elevation"),
    "geoposName": fields.String( description="internal field"),
})

wigosid = api.model('WIGOS identifier' ,{
    'id': fields.Integer(readOnly=True, description='The unique identifier of a wigosid'),
    'wid': fields.String(required=True, description="Station description"),
    'primary' : fields.Boolean(description="WIGOS identifier")
})

description = api.model('Station description' ,{
    'id': fields.Integer(readOnly=True, description='The unique identifier of a description'),
    'validSince': fields.DateTime(required=True,description='validity date of description'),
    'description': fields.String(required=True, description="Station description"),
})

observation = api.model('Observation' ,{
    'id': fields.Integer(readOnly=True, description='The unique identifier of an observation'),
    'variableName': fields.String(required=True, description="variable name"),
    'geometryName': fields.String(required=True, description="geometry name"),
    'lastModifiedOn' : fields.DateTime(description="last modification date/time"),
    'programs' : fields.List(fields.Nested(program))
})

station = api.model('Oscar Station', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a station'),
    'name': fields.String(required=True, description='Station name'),
    'wmoRaName': fields.String(required=True, description='WMO Region'),
    'typeName': fields.String(required=True, description='Station type'),
    'typeName': fields.String(required=True, description='Station type'),
    'dateEstablished': fields.DateTime,
    'observations': fields.List(fields.Nested(observation),required=True),    
    'descriptions': fields.List(fields.Nested(description)),
    'locations' : fields.List(fields.Nested(location),required=True),
    'timezones' : fields.List(fields.Nested(timezone),required=True),
    'territories' : fields.List(fields.Nested(territory),required=True),
    'wigosIds' : fields.List(fields.Nested(wigosid),required=True),
    'stationPrograms' : fields.List(fields.Nested(program),required=True)
})

station_search = api.model('Oscar Station in search', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a station'),
    'name': fields.String(required=True, description='Station name'),
    'wmoIndex': fields.String(required=True, description='Station identifier'),
    'region': fields.String(required=True, description='WMO region'),
    'territory': fields.String(required=True, description='WMO Member'),
    'longitude': fields.Float(required=True, description='Longitude of station'),
    'latitude': fields.Float(required=True, description='Latitude of station'),
    'elevation': fields.Integer(required=True, description='Latitude of station'),
    'stationTypeName': fields.String(required=True, description='Station type'),
    'stationTypeId': fields.Integer(required=True, description='Station type id'),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})


