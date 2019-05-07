"""Core Appliction.
This module houses the core Flask application.
"""

import json
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# POSTGRES_USER = 'brighthive'
# POSTGRES_PASSWORD = 'test_password'
# POSTGRES_DATABASE = 'mci_dev'
# # POSTGRES_HOSTNAME= 'postgres_mci' 
# # Attempt 1: hostname = the name of the service in the docker-compose file
# # https://stackoverflow.com/questions/50627399/docker-compose-app-container-cant-connect-to-postgres
# POSTGRES_HOSTNAME = 'localhost'
# POSTGRES_PORT = '5434'
# SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
#     POSTGRES_USER,
#     POSTGRES_PASSWORD,
#     POSTGRES_HOSTNAME,
#     POSTGRES_PORT,
#     POSTGRES_DATABASE
# )

# engine = create_engine(SQLALCHEMY_DATABASE_URI)

# metadata = MetaData(bind=engine)

# from sqlalchemy import Table

# individual = Table('individual', metadata, autoload=True)

api = Api(app)

from matching.api import ComputeMatch
api.add_resource(ComputeMatch, '/compute-match')