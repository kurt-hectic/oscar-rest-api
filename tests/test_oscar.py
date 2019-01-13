import os
from rest_api_oscar import app as oscar_app
import pytest
import tempfile
import json
import random, string

@pytest.fixture(scope='module')
def client():
    
    oscar_app.app.config['TESTING'] = True
    client = oscar_app.app.test_client()

    yield client

@pytest.fixture(scope='module')
def token():
    
    oscar_app.app.config['TESTING'] = True
    client = oscar_app.app.test_client()
    
    params = { 'username': 'tproescholdt@wmo.int' , 'password': 'Oscar4ever!' }
    r = client.post('/api/auth/login' , json=params )
    
    response = json.loads(r.data)
    token = response["token"]
    
    yield token
    
    
def test_station_list(client):
    """test if a station list is returned"""
    r = client.get('/api/stations/')
    station_list = json.loads(r.data)
    assert "dateEstablished" in station_list[0]
    
    
def test_station_present(client):
    """test if a station can be retrieved"""
    r = client.get('/api/stations/4618')
    assert b'VLADIMIR' in r.data   
    
def test_login(client):
    """test succesfull login into OSCAR"""
    params = { 'username': 'tproescholdt@wmo.int' , 'password': 'Oscar4ever!' }
    r = client.post('/api/auth/login' , json=params )
    assert r.status_code == 200

def test_failed_login(client):
    """test unsuccesfull login into OSCAR"""
    params = { 'username': 'tproescholdt@wmo.int' , 'password': 'Oscar4never!' }
    r = client.post('/api/auth/login' , json=params )
    assert r.status_code == 401

def test_search(client):
    """test searching"""
    r = client.get('/api/stations/search?wmoRegion=europe')
    station_list = json.loads(r.data)
    first_station = station_list[0]
    assert first_station["region"] == "Europe"
    

def test_create(client,token):
    """test creating a station """
    
    minimal_station = json.loads("""
    { 	"typeName": "Land (fixed)", 	"locations": [{ 		"validSince": "2019-01-01", 		"latitude": "10.0000", 		"longitude": "20.0000", 		"elevation": 123 	}], 	"name": "TIMO TEST 101", 	"wigosIds": [{ 		"wid": "0-20000-0-timo-test" 	}], 	"dateEstablished": "2019-01-01", 	"wmoRaName": "VI - Europe", 	"territories": [{ 		"validSince": "2019-01-01", 		"territoryName": "Albania" 	}], 	"timezones": [{ 		"timezoneName": "UTC+1", 		"validSince": "2019-01-01" 	}], 	"stationPrograms": [{ 		"program": "Non-affiliated" 	}], 	"observations": [{ 		"programs": [{ 			"program": "Non-affiliated" 		}], 		"variableName": "Integrated air samples", 		"geometryName": "Point" 	}] }   
    
    """)
    
    name_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    minimal_station["name"] += name_suffix
    minimal_station["wigosIds"][0]["wid"] += name_suffix
    
    headers = { "X-OSCAR-api-token"  :  token }
    
    r = client.post('/api/stations/' ,  headers=headers , json=minimal_station )
    assert r.status_code == 201
    
def test_create_fail(client,token):
    """test creating a station with invalid data"""
    
    minimal_station_no_name = json.loads("""
    { 	"typeName": "Land (fixed)", 	"locations": [{ 		"validSince": "2019-01-01", 		"latitude": "10.0000", 		"longitude": "20.0000", 		"elevation": 123 	}], 	"wigosIds": [{ 		"wid": "0-20000-0-timo-test" 	}], 	"dateEstablished": "2019-01-01", 	"wmoRaName": "VI - Europe", 	"territories": [{ 		"validSince": "2019-01-01", 		"territoryName": "Albania" 	}], 	"timezones": [{ 		"timezoneName": "UTC+1", 		"validSince": "2019-01-01" 	}], 	"stationPrograms": [{ 		"program": "Non-affiliated" 	}], 	"observations": [{ 		"programs": [{ 			"program": "Non-affiliated" 		}], 		"variableName": "Integrated air samples", 		"geometryName": "Point" 	}] }   
    
    """)
    
    name_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    minimal_station_no_name["wigosIds"][0]["wid"] += name_suffix
    
    headers = { "X-OSCAR-api-token"  :  token }    
    r = client.post('/api/stations/' ,  headers=headers , json=minimal_station_no_name )

    assert r.status_code == 400
    assert "is a required property" in  r.data.decode() 
    