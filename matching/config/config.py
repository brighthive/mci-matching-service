import os


class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'development'

    DEBUG = True

    POSTGRES_USER = 'brighthive'
    POSTGRES_PASSWORD = 'test_password'
    POSTGRES_DATABASE = 'mci_dev'
    POSTGRES_PORT = '5432'
    # POSTGRES_HOSTNAME = 'localhost'
    POSTGRES_HOSTNAME = 'docker_postgres_mci_1'
    # If the matching-service is running in a Docker container, then connect to the
    # mci psql container, rather than localhost.
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )


class TestConfig(Config):
    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'test'

    DEBUG = True

    POSTGRES_USER = 'brighthive'
    POSTGRES_PASSWORD = 'test_password'
    POSTGRES_DATABASE = 'mci_dev'
    POSTGRES_HOSTNAME = 'localhost'
    POSTGRES_PORT = '5436'  # Do not use 5432, since it may be allocated.
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'production'

    DEBUG = False
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'brighthive')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'test_password')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'mci_test')
    POSTGRES_HOSTNAME = os.getenv('POSTGRES_HOSTNAME', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )


class ConfigurationFactory(object):
    """Application configuration factory.
    This factoty class provides a quick and easy mechanism for retrieving a specific configuration
    type without the need for manually creating configuration objects.
    """

    @staticmethod
    def get_config(config_type: str):
        """Return a configuration by it's type.
        Primary factory method that returns a configuration object based on the provided configuration type.
        Args:
            config_type (str): Configuration factory type return. May be one of:
                - TEST
                - DEVELOPMENT
                - INTEGRATION
                - SANDBOX
                - PRODUCTION
        Returns:
            object: Configuration object based on the specified config_type.
        """
        if config_type.upper() == 'TEST':
            return TestConfig()
        elif config_type.upper() == 'DEVELOPMENT':
            return DevelopmentConfig()
        elif config_type.upper() == 'PRODUCTION':
            return ProductionConfig()

    @staticmethod
    def from_env():
        """Retrieve configuration based on environment settings.
        Provides a configuration object based on the settings found in the `APP_ENV` variable. Defaults to the `development`
        environment if the variable is not set.
        Returns:
            object: Configuration object based on the configuration environment found in the `APP_ENV` environment variable.
        """
        environment = os.getenv('APP_ENV', 'TEST')

        return ConfigurationFactory.get_config(environment)
