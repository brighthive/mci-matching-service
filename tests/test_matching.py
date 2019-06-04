import pytest
import json

from matching.database import engine, init_individual_table

def test_get_endpoint(client, app):
    response = client.get('/compute-match')

    assert response.status_code == 200

def test_user_match_exact(
        client, 
        app, 
        psql_docker, 
        individual_data,
        address_insert,
        gender_insert
    ):
    psql_docker.setup_postgres_container()

    engine.execute(gender_insert)
    engine.execute(address_insert)
    individual = init_individual_table()
    engine.execute(individual.insert(), **individual_data)
    response = client.post('/compute-match', data=json.dumps(individual_data))
    
    psql_docker.teardown_postgres_container()

    assert response.status_code == 201
    assert response.get_json()['mci_id'] == individual_data['mci_id']
    assert response.get_json()['score'] == 1.0


@pytest.mark.parametrize('date_of_birth,last_name,first_name,telephone,email_address,mailing_address_id,gender_id,score', [
    ('2019-01-01', 'Handel', '', '', '', '', '', ''),
    ('1985-01-01', 'Scarlatti', '', '', '', '', '', ''),
    ('1985-01-01', 'Handel', '', '', '', '', '', 0.4),
    ('1985-01-01', 'Handel', 'George', '', '', '', '', 0.55),
    ('1985-01-01', 'Handel', 'George', '123-456-7890', '', '', '', 0.65),
    ('1985-01-01', 'Handel', 'George', '123-456-7890', 'handel@hotmail.com', '', '', 0.75),
    ('1985-01-01', 'Handel', 'George', '123-456-7890', 'handel@hotmail.com', '1', '', 0.85),
    ('1985-01-01', 'Handel', 'George', '123-456-7890', 'handel@hotmail.com', '1', '1', 0.90),
])
def test_user_match(
        client, 
        app, 
        psql_docker, 
        individual_data,
        address_insert,
        gender_insert,
        date_of_birth,
        last_name,
        first_name,
        telephone,
        email_address,
        mailing_address_id,
        gender_id,
        score
    ):
    psql_docker.setup_postgres_container()

    engine.execute(gender_insert)
    engine.execute(address_insert)
    individual = init_individual_table()
    engine.execute(individual.insert(), **individual_data)
    response = client.post('/compute-match', data=json.dumps(individual_data))

    incoming_data = {
        'date_of_birth': date_of_birth,
        'last_name': last_name,
        'first_name': first_name,
        'telephone': telephone,
        'email_address': email_address,
        'mailing_address_id': mailing_address_id,
        'gender_id': gender_id,
    }
    response = client.post('/compute-match', data=json.dumps(incoming_data))

    psql_docker.teardown_postgres_container()

    assert response.status_code == 201
    assert response.get_json()['score'] == score
