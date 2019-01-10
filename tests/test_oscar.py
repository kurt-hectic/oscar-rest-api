import os
from rest_api_oscar import app as oscar_app
import pytest
import tempfile
import json

@pytest.fixture(scope='module')
def client():
    
    oscar_app.app.config['TESTING'] = True
    client = oscar_app.app.test_client()

    with oscar_app.app.app_context():
        oscar_app.initialize_app(oscar_app.app)

    yield client

def test_station_present(client):
    """test if a station can be retrieved"""

    r = client.get('/api/stations/4618')
    assert b'VLADIMIR' in r.data   
    
def test_login(client):
    """test succesfull login into OSCAR"""
    params = { 'username': 'tproescholdt@wmo.int' , 'password': 'Oscar4ever!' }
    r = client.post('/api/auth/login' , json=params )
    assert r.status_code == 200

def test__failed_login(client):
    """test unsuccesfull login into OSCAR"""
    params = { 'username': 'tproescholdt@wmo.int' , 'password': 'Oscar4never!' }
    r = client.post('/api/auth/login' , json=params )
    assert r.status_code == 401

