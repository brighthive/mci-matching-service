'''
This module provides the POST endpoint for finding matches.
'''
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

from matching.common.util import compute_mci_threshold

individual_args = {
    'first_name': fields.Str(),
    'date_of_birth': fields.Str(),
    'last_name': fields.Str(),
    'gender': fields.Str(),
    'email': fields.Str(),
    'telephone': fields.Str(),
    'mailing_address_id': fields.Str(),
    'ssn': fields.Str(),
    # 'mailing_address': fields.Nested(
    #     {
    #         "address": fields.Str(), 
    #         "city": fields.Str(), 
    #         "state": fields.Str(), 
    #         "postal_code": fields.Str(), 
    #         "country": fields.Str(),
    #     }
    # ),
}

class ComputeMatch(Resource):
    @use_args(individual_args)
    def post(self, args):
        match, score = compute_mci_threshold(args)
        
        return {'score': score}, 201
