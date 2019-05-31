import time
from io import BytesIO
import os
import subprocess

import docker
import pytest

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
        # cleanup old containers
        try:
            container_to_clean = self.docker_client.containers.get(self.container_name)
            container_to_clean.stop()
            container_to_clean.remove()
        except docker.errors.NotFound:
            print('Container not found.')
        # download Docker PostgreSQL image for unit testing only
        try:
            print('Launching Docker PostgreSQL Container...')
            self.docker_client.images.pull(self.postgres_image)
        except Exception as err:
            print(err)
            print('Failed to retrieve PostgreSQL image!')

        # launch Docker PostgreSQL image for unit testing only
        db_environment = [
            'POSTGRES_USER={}'.format('brighthive'),
            'POSTGRES_PASSWORD={}'.format('test_password'),
            'POSTGRES_DB={}'.format('mci_dev')
        ]

        try:
            self.docker_client.containers.run(
                self.postgres_image,
                detach=True,
                auto_remove=True,
                name=self.container_name,
                ports={'5432/tcp': '5436'},
                environment=db_environment,
                tmpfs={'/tmp/mci_models.tar': ''},
            )


            import os
            from flask import Flask
            from flask_migrate import upgrade
            from flask_migrate import Migrate

            # Made possible by: pipenv install ../master-client-index/dist/mci-1.0.tar.gz
            from mci import db
            
            # Borrowed from: https://github.com/pallets/flask/blob/master/tests/conftest.py#L61
            app = Flask("flask_test", root_path=os.path.dirname(__file__))

            migrate = Migrate(app, db)
            
            app.config.from_mapping(
                TESTING = True,
                SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
                    'brighthive',
                    'test_password',
                    'localhost',
                    5436,
                    'mci_dev')
            )
            
            with app.app_context():
                

                path_to_virtual_env = os.environ['VIRTUAL_ENV']
                # N.b, this path makes sense on my machine, only...
                migrations_dir = os.path.join(
                            path_to_virtual_env, 'lib/python3.7/site-packages', 'mci', 'db', 'migrations')

                # TODO: Wait? Or while loop?
                import time
                time.sleep(2)

                upgrade(directory=migrations_dir)

            # A container with tables! Ready for population with fixtures!
            psql_container = self.docker_client.containers.get('postgres_test')    



        except Exception as err:
            print(err)
            print('Unable to start container...')

    def teardown_postgres_container(self):
        """Teardown Dockerr PostgreSQL container.
        Spins down the Docker PostgreSQL testing container.
        """
        print('Tearing Down Docker PostgreSQL Container...')
        try:
            container = self.docker_client.containers.get(self.container_name)
            container.stop()
        except Exception:
            print('Unable to stop container...'.format(self.container_name))


@pytest.fixture()
def psql_docker():
    """Database container."""
    return PostgreSQLContainer()


@pytest.fixture
def app(psql_docker):
    # Set up existing psql container, before running app.
    psql_docker.setup_postgres_container()

    from matching import app as application

    return application
