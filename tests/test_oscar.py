import os
from rest_api_oscar import app as oscar_app
import pytest
import tempfile
import json

@pytest.fixture
def client():
    
    oscar_app.app.config['TESTING'] = True
    client = oscar_app.app.test_client()

    with oscar_app.app.app_context():
        oscar_app.initialize_app(oscar_app.app)

    yield client

def test_empty_(client):
    """Start with a blank database."""

    rv = client.get('/api/stations/4618')
    assert b'VLADIMIR' in rv.data