from flask_restplus import fields
from rest_api_oscar.api.restplus import api

station = api.model('Oscar Station', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a station'),
    'name': fields.String(required=True, description='Station name'),
    'date_established': fields.DateTime
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})
