"""Core Appliction.
This module houses the core Flask application.
"""

import json
import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base

from matching.api import ComputeMatch
from matching.config import ConfigurationFactory

app = Flask(__name__)
app.config.from_object(ConfigurationFactory.from_env())
api = Api(app)

api.add_resource(ComputeMatch, '/compute-match')
