import pytest
import json


def test_the_truth():

    assert True == True

def test_get_endpoint(client, app):
    response = client.get('/compute-match')

    assert response.status_code == 200

def test_user_match_ninety(client, app, individual_data):
    from matching.database import engine, individual

    engine.execute(individual.insert(), **individual_data)

    response = client.post('/compute-match', data=json.dumps(individual_data))

    assert response.status_code == 201
    assert response.get_json()['mci_id'] == individual_data['mci_id']
    assert response.get_json()['score'] == 0.9


def test_user_match_forty(client, app, individual_data):
    from matching.database import engine, individual
    # http: // flask.pocoo.org/docs/1.0/patterns/sqlalchemy/
    engine.execute(individual.insert(), **individual_data)

    poor_match = {
        'date_of_birth': individual_data['date_of_birth'],
        'last_name': individual_data['last_name']
    }
    response = client.post('/compute-match', data=json.dumps(poor_match))

    assert response.status_code == 201
    assert response.get_json()['score'] == 0.4
