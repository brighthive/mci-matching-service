"""Core Appliction.
This module houses the core Flask application.
"""

import json
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from matching.api import ComputeMatch
api.add_resource(ComputeMatch, '/compute-match')