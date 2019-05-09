'''
This module provides the POST endpoint for finding matches.
'''
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

from matching.common.util import compute_match_with_score

individual_args = {
    'first_name': fields.Str(),
    'date_of_birth': fields.Str(),
    'last_name': fields.Str(),
    'gender_id': fields.Str(),
    'email_address': fields.Str(),
    'telephone': fields.Str(),
    'mailing_address_id': fields.Str(),
    'ssn': fields.Str(),
}

class ComputeMatch(Resource):
    # Keeping this as a sanity-check placeholder, for now.
    def get(self):
        return {'hello': 'world'}

    @use_args(individual_args)
    def post(self, args):
        mci_id, score = compute_match_with_score(args)
        
        return {'mci_id': mci_id, 'score': score}, 201
