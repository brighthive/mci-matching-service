import pytest

def test_the_truth():

    assert True == True

def test_get_endpoint(client, app):
    response = client.get('/compute-match')

    assert response.status_code == 200
