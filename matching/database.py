from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy
from flask import g
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from matching.config import ConfigurationFactory

config = ConfigurationFactory.from_env()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))

def init_individual_table():
    '''
    This function abstracts a Table with Individual metadata from the MCI database.

    References:
    - http://flask.pocoo.org/docs/1.0/patterns/sqlalchemy/#sql-abstraction-layer
    - https://docs.sqlalchemy.org/en/13/core/metadata.html
    '''
    metadata = MetaData(bind=engine)
    individual = Table('individual', metadata, autoload=True)

    return individual
