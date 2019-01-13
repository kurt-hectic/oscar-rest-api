import logging

from flask import request, current_app
from flask_restplus import Resource, fields
from rest_api_oscar.oscarlib.oscar_saml import OscarSaml 
from rest_api_oscar.api.restplus import api
import json
from flask import jsonify

import rest_api_oscar.api.oscar.utils as tokenutils

ns = api.namespace('auth', description='Operations related to OSCAR login')

log = logging.getLogger(__name__)

user_auth = api.model('auth_details', {
    'username': fields.String(required=True, description='The username '),
    'password': fields.String(required=True, description='The user password '),
})


@ns.route('/credentials')
class CredentialsOperation(Resource):
    
    @api.doc(security='apikey')    
    @api.doc('obtain credentials')
    @api.response(401, 'token not accepted')
    @api.response(200, 'token ok, return user details')    
    def get(self,token):
        """obtain user information"""

        try:
            token = request.headers.get(tokenutils.OSCAR_TOKEN)        
            if not token:
                return {'logout' : False }, 401
            
            [cookies,qlack_token] = tokenutils.decode_token(token)
            
            log.debug("obtained cookies: {} token: {}".format(cookies,qlack_token))
            oscar_client = OscarSaml(oscarurl=current_app.config["OSCAR_URL"])
            
            user_details = oscar_client.getUserCredentials(cookies,qlack_token)
        
            if user_details:
                return user_details, 200
            else:
                return False, 401
        except Exception as e:
            return "processing error: {}".format(e), 500
        
@ns.route('/login')
class LoginOperation(Resource):

    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    @api.response(401, 'Not authorized')
    @api.response(200, 'Login OK')
    def post(self):
        """login into OSCAR"""
        params = request.json
        oscar_client = OscarSaml(oscarurl=current_app.config["OSCAR_URL"])

        session_info =  oscar_client.performLogin(params["username"],params["password"]) 
        log.debug("session info")
        if session_info:
            token = tokenutils.encode_token( session_info )
            return { 'login' : True , 'token' : token }, 200
        else:
            return { 'login' : False }, 401

@ns.route('/logout')
class LogoutOperation(Resource):

    @api.doc(security='apikey')    
    @api.doc('user logout')
    @api.response(401, 'Not authorized')
    @api.response(200, 'Logout OK')
    def delete(self):
        """Destroys the session"""
   
        token = request.headers.get(OSCAR_TOKEN)        
        if not token:
            return {'logout' : False }, 401
   
        [cookies,qlack_token] = tokenutils.decode_token(token)
        
        log.debug("obtained cookies: {} token: {}".format(cookies,qlack_token))
        oscar_client = OscarSaml(oscarurl=current_app.config["OSCAR_URL"])
        
        if oscar_client.performLogout(cookies,qlack_token):
            return {'logout' : True }, 200
        else:
            return {'logout' : False }, 401