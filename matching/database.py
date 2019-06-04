from flask_sqlalchemy import SQLAlchemy
from flask import g
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from matching.config import ConfigurationFactory

config = ConfigurationFactory.from_env()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

def init_individual_table():
    # Instantiate a Table with Metadata
    # http://flask.pocoo.org/docs/1.0/patterns/sqlalchemy/#sql-abstraction-layer
    # https://docs.sqlalchemy.org/en/13/core/metadata.html
    metadata = MetaData(bind=engine)
    individual = Table('individual', metadata, autoload=True)

    return individual

def init_db_session():
    # https://docs.sqlalchemy.org/en/13/orm/contextual.html#using-thread-local-scope-with-web-applications
    # Pass the engine to the sessionmaker (a factory for creating sessions, 
    # i.e., a object that manages interactions with the database) 
    # https://docs.sqlalchemy.org/en/13/orm/session_basics.html#what-does-the-session-do
    Session = scoped_session(sessionmaker(bind=engine))
    # Register the session
    Session()
    # Add session to "g"
    g.mci_db_session = Session

    return Session
