from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker

# Instantiate the engine – the "home base" for the database
from matching.config import ConfigurationFactory
config = ConfigurationFactory.from_env()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

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
