'''
This module provides the POST endpoint for finding matches.
'''
from flask_restful import Resource

class ComputeMatch(Resource):
    def get(self):
        return {'hello': 'world'}