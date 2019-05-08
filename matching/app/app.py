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
api = Api(app)

from matching.api import ComputeMatch
api.add_resource(ComputeMatch, '/compute-match')