import os
import subprocess

import docker
import pytest

from matching import app as application
from matching.config import ConfigurationFactory

environment = os.getenv('APP_ENV', 'TEST')
config = ConfigurationFactory.get_config(environment.upper())
docker_client = docker.from_env()
postgres_image = "postgres:11.2"
container_name = "postgres_test"

def setup_postgres_container():
    """Setup Docker PostgreSQL container.
    Spins up a Docker PostgreSQL container for testing.
    """
    # download Docker PostgreSQL image for unit testing only
    try:
        print('Launching Docker PostgreSQL Container...')
        docker_client.images.pull(postgres_image)
    except Exception as err:
        print(err)
        print('Failed to retrieve PostgreSQL image!')

    # launch Docker PostgreSQL image for unit testing only
    db_environment = [
        'POSTGRES_USER={}'.format(config.POSTGRES_USER),
        'POSTGRES_PASSWORD={}'.format(config.POSTGRES_PASSWORD),
        'POSTGRES_DB={}'.format(config.POSTGRES_DATABASE)
    ]
    try:
        docker_client.containers.run(
            postgres_image,
            detach=True,
            auto_remove=True,
            name=container_name,
            ports={'5432/tcp': config.POSTGRES_PORT},
            environment=db_environment,
        )
        import pdb; pdb.set_trace()
    except Exception as err:
        print(err)
        print('Unable to start container...')

    # TODO: Set-up a database.
    # Option – restore a db dump?
    # Option – somehow run the migrations from the MCI repo in this repo?
    
def teardown_postgres_container():
    """Teardown Dockerr PostgreSQL container.
    Spins down the Docker PostgreSQL testing container.
    """
    print('Tearing Down Docker PostgreSQL Container...')
    try:
        container = docker_client.containers.get(container_name)
        container.stop()
    except Exception:
        print('Unable to stop container...'.format(container_name))


@pytest.fixture
def database():
    """Database fixture."""
    setup_postgres_container()
    teardown_postgres_container()


@pytest.fixture
def app():
    return application
