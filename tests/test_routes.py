from flask import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_get_routes(client):
    response = client.get('/api/some_endpoint')  # Replace with actual endpoint
    assert response.status_code == 200
    assert 'expected_key' in json.loads(response.data)

def test_post_routes(client):
    response = client.post('/api/some_endpoint', json={'key': 'value'})  # Replace with actual endpoint and data
    assert response.status_code == 201
    assert 'expected_key' in json.loads(response.data)

def test_invalid_route(client):
    response = client.get('/api/invalid_endpoint')  # Replace with an invalid endpoint
    assert response.status_code == 404