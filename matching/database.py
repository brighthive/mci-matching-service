from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = 'brighthive'
POSTGRES_PASSWORD = 'test_password'
POSTGRES_DATABASE = 'mci_dev'
POSTGRES_HOSTNAME = 'localhost'
POSTGRES_PORT = '5434'
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOSTNAME,
    POSTGRES_PORT,
    POSTGRES_DATABASE
)

# Instantiate the engine – the "home base" for the database
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Pass the engine to the sessionmaker (a factory for creating sessions, 
# i.e., a object that manages interactions with the database) 
# https://docs.sqlalchemy.org/en/13/orm/session_basics.html#what-does-the-session-do
Session = sessionmaker(bind=engine)
session = Session()

# Instantiate a Table with Metadata
# http://flask.pocoo.org/docs/1.0/patterns/sqlalchemy/#sql-abstraction-layer
# https://docs.sqlalchemy.org/en/13/core/metadata.html
metadata = MetaData(bind=engine)
individual = Table('individual', metadata, autoload=True)