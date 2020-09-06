'''
This module provides the POST endpoint for finding matches.
'''
from flask_restful import Resource, request
from webargs import fields
from webargs.flaskparser import use_args

from matching.common.util import compute_match_with_score


class ComputeMatch(Resource):
    # Keeping this as a sanity-check placeholder, for now.
    def get(self):
        return {'hello': 'world'}

    # @use_args(individual_args)
    def post(self):
        mci_id, score = compute_match_with_score(request.get_json(force=True))
        return {'mci_id': mci_id, 'score': score}, 201
