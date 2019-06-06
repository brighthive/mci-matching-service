import os
import subprocess
import time
from io import BytesIO
from time import sleep

import docker
import pytest
from flask import Flask
from flask_migrate import Migrate, upgrade

from matching import app as application
from matching.config import TestConfig as config
from mci_database import db

MAX_RETRIES = 10
SLEEP = 2

class PostgreSQLContainer(object):
    """A PostgreSQL Container Object.
    This class provides a mechanism for managing PostgreSQL Docker containers
    so that it can be injected into unit tests.
    Class Attributes:
        config (object): A Configuration Factory object.
        container (object): The Docker container object.
        docker_client (object): Docker client.
        db_environment (list): Database environment configuration variables.
        db_ports (dict): Dictionary of database port mappings.
    """

    def __init__(self):
        self.docker_client = docker.from_env()
        self.postgres_image = "postgres:11.2"
        self.container_name = "postgres_test"

    def setup_postgres_container(self):
        """Setup Docker PostgreSQL container.
        Spins up a Docker PostgreSQL container for testing.
        """
        try:
            self.teardown_postgres_container()
        except docker.errors.NotFound:
            print('Container not found!')

        self.docker_client.images.pull(self.postgres_image)

        self.docker_client.containers.run(
            self.postgres_image,
            detach=True,
            auto_remove=True,
            name=self.container_name,
            ports={'5432/tcp': '5436'},
            environment=[
                'POSTGRES_USER={}'.format(config.POSTGRES_USER),
                'POSTGRES_PASSWORD={}'.format(config.POSTGRES_PASSWORD),
                'POSTGRES_DB={}'.format(config.POSTGRES_DATABASE),
                'POSTGRES_HOSTNAME={}'.format(config.POSTGRES_HOSTNAME),
            ],
            tmpfs={'/tmp/mci_models.tar': ''},
        )
        
        # Borrowed from: https://github.com/pallets/flask/blob/master/tests/conftest.py#L61
        app = Flask("flask_test", root_path=os.path.dirname(__file__))

        migrate = Migrate(app, db)
        
        app.config.from_mapping(
            TESTING = True,
            SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI,
        )
        
        applied_migrations = False
        retries = 0

        with app.app_context():
            # The migrations repo resides in the virtual env.
            # Specifically, Pipenv installs the mci-database repo in the `src` directory,
            # since the Pipfile marks it as "editable."
            path_to_virtual_env = os.environ['VIRTUAL_ENV']
            migrations_dir = os.path.join(
                path_to_virtual_env, 'src', 'mci-database', 'mci_database', 'db', 'migrations')

            while retries < MAX_RETRIES and applied_migrations is False:
                print('Attempting to apply migrations ({} of {})...'.format(
                    retries + 1, MAX_RETRIES))
                try:
                    # apply the migrations
                    upgrade(directory=migrations_dir)
                    applied_migrations = True
                except Exception:
                    retries += 1
                    sleep(SLEEP)

        print('Container launched!')

    def teardown_postgres_container(self):
        """Teardown Dockerr PostgreSQL container.
        Spins down the Docker PostgreSQL testing container.
        """
        print('Stopping and removing Docker PostgreSQL Container...')
        container_to_clean = self.docker_client.containers.get(
            self.container_name)
        container_to_clean.stop()


@pytest.fixture()
def psql_docker():
    return PostgreSQLContainer()


@pytest.fixture()
def individual_data(psql_docker):    
    individual_data = {
        'mci_id': '1qaz2wsx3edc',
        'ssn': '123456789',
        'first_name': 'George',
        'last_name': 'Handel',
        'middle_name': 'Frideric',
        'date_of_birth': '1985-01-01',
        'email_address': 'handel@hotmail.com',
        'telephone': '123-456-7890',
        'gender_id': '1',
        'mailing_address_id': '1',
    }

    return individual_data


@pytest.fixture
def address_insert():
    insert_statement = '''
    INSERT INTO address (address, city, state, postal_code, country) 
    VALUES ('123 Main St', 'City', 'State', '12345', 'US')
    '''

    return insert_statement


@pytest.fixture
def gender_insert():
    return "INSERT INTO gender (gender) VALUES ('woman')"


@pytest.fixture
def app(psql_docker):
    return application
