'''
This module provides the POST endpoint for finding matches.
'''
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

from matching.common.util import compute_mci_threshold

individual_args = {"first_name": fields.Str()}

class ComputeMatch(Resource):
    @use_args(individual_args)
    def post(self, args):
        match, score = compute_mci_threshold(args)
        
        return {'score': score}, 201