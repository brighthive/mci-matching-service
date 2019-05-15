"""Core Appliction.
This module houses the core Flask application.
"""

from flask import Flask
from flask_restful import Api

from matching.api import ComputeMatch
from matching.config import ConfigurationFactory

app = Flask(__name__)
app.config.from_object(ConfigurationFactory.from_env())
api = Api(app)

api.add_resource(ComputeMatch, '/compute-match')
