'''
This module provides the POST endpoint for finding matches.
'''
from flask_restful import Resource, reqparse

class ComputeMatch(Resource):
    def post(self):
        '''
        Integrate compute_mci_threshold here!
        This resource should accept JSON with the Individual data, e.g., dob, 
        first_name, last_name, etc. Then, it will parse the data, do the calculation, and
        return a result.
        '''
        # https://flask-restful.readthedocs.io/en/0.3.5/quickstart.html#full-example
        parser = reqparse.RequestParser()
        parser.add_argument('first_name')
        args = parser.parse_args()

        # for testing that the POST behaves as expected
        result = {'match': args['first_name'] , 'score': ''}
        
        return result, 201