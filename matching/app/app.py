"""Core Appliction.
This module houses the core Flask application.
"""

from flask import Flask, g
from flask_restful import Api

from matching.api import ComputeMatch
from matching.config import ConfigurationFactory
from matching.database import Session

app = Flask(__name__)
app.config.from_object(ConfigurationFactory.from_env())

api = Api(app)
api.add_resource(ComputeMatch, '/compute-match')

@app.teardown_appcontext
def cleanup(resp_or_exc):
    '''
    A session establishes all conversations with the database. 
    Mainly, it requests a connection with the database. 
    
    A session can have a lifespan across many *short* transactions. For web applications, 
	the scope of a session should align with the scope of a request. 
	In other words: tear down the session at the end of a request.

	This decorator function ensures that Sessions are removed at the end of a request.

	References:
	- https://docs.sqlalchemy.org/en/13/orm/contextual.html#using-thread-local-scope-with-web-applications
	- https://dev.to/nestedsoftware/flask-and-sqlalchemy-without-the-flask-sqlalchemy-extension-3cf8
    '''
    Session.remove()
