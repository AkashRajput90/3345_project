# test_application.py

from app import app
import pytest

# Example test to check if the index route returns a 200 status code
def test_index_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
