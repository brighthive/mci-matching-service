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

            # 1. RUN COMMAND AS SUBPROCESS
            # import subprocess
            # command = 'cat /Users/reginacompton/Downloads/colorado_sample_mci.sql | docker exec -i postgres_test psql -U brighthive -d mci_dev'
            # p = subprocess.Popen(command, shell=True)

            # 2. ADD DUMP TO CONTAINER AND RESTORE
            # https: // gist.github.com/zbyte64/6800eae10ce082bb78f0b7a2cca5cbc2

            # data = open('/Users/reginacompton/brighthive/mci-matching-service/tests/mci_models.dump', 'rb').read()

            # psql_container = self.docker_client.containers.get('postgres_test')

            # psql_container.put_archive(path='/tmp', data=data)
            # psql_container.exec_run('pg_restore -U brighthive -Ft /tmp/mci_models.tar')

            # 3. USE EXEC_RUN
            # psql_container.exec_run('cat /tmp/mci_models.tar | psql -U brighthive -d mci_dev')

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
