"""Core Appliction.
This module houses the core Flask application.
"""

from flask import Flask, g
from flask_restful import Api

from matching.api import ComputeMatch
from matching.config import ConfigurationFactory

app = Flask(__name__)
app.config.from_object(ConfigurationFactory.from_env())

api = Api(app)
api.add_resource(ComputeMatch, '/compute-match')

@app.teardown_appcontext
def close_db_session(error):
    """Closes the database session at the end of the request."""
    if hasattr(g, 'mci_db_session'):
        g.mci_db_session.remove()
