from itertools import combinations

from sqlalchemy import String, cast

from matching.database import engine, individual, session

def filter_on_ssn(combo, potential_matches):
    '''
    Helper function used in `compute_match_with_score`.
    '''
    if combo.get('ssn'):
        ssn_last_four_digits = combo.get('ssn')[-4:]
        del(combo['ssn'])
        match = potential_matches.filter_by(**combo)\
                                 .filter(cast(individual.c.ssn, String)
                                 .like('%{}'.format(ssn_last_four_digits)))
    else:
        match = potential_matches.filter_by(**combo)
    
    return match

def compute_match_with_score(individual_args: dict):
    '''
    This function determines (1) if incoming data for an Individual
    can be reasonably matched with an existing entry, and (2) the
    score assigned to the likelihood of matching. 

    The `last_name` and `date_of_birth` are weighted at 0.2 (or 0.4 together)
    and each remaining field is weighted at 0.15, 0.1, or 0.05 (with `gender_id` having the lowest weight). 
    Note! The precise weights for these fields will be fine tuned, as we come 
    to understand the data better.

    :param individual_args: a dict of Individual data that includes, at minimum, a
    `last_name` and `date_of_birth`.

    :returns: an Individual and a score of the match likelihood (or None) 
    '''

    mci_id = ''
    score = ''
    gender_id = individual_args.get('gender_id')
    mailing_address_id = individual_args.get('mailing_address_id')
    filters = {
        'first_name': individual_args.get('first_name', None) or None,
        'telephone': individual_args.get('telephone', None) or None,
        'email_address': individual_args.get('email_address', None) or None,
        'mailing_address_id': int(mailing_address_id) if mailing_address_id else None,
        'ssn': individual_args.get('ssn', None) or None,
        'gender_id': int(gender_id) if gender_id else None,
    }

    weights = {
        'first_name': 0.15,
        'telephone': 0.1,
        'email_address': 0.1,
        'mailing_address_id': 0.1,
        'ssn': 0.1,
        'gender_id': 0.05,
    }

    potential_matches = session.query(individual).filter_by(
        last_name=individual_args['last_name'],
        date_of_birth=individual_args['date_of_birth']
    )

    if potential_matches.first():
        score = 0.4
        list_of_combos = []
        # Find all filter combinations.
        # Reference: https://stackoverflow.com/questions/11905573/getting-all-combinations-of-key-value-pairs-in-python-dict
        for i in range(len(filters), 0, -1):
            list_of_combos += list(map(dict, combinations(filters.items(), i)))

        for combo in list_of_combos:
            combo_length_for_score = len(combo)
            match = filter_on_ssn(combo, potential_matches)

            if match.first():
                # TO TEST: in what cases can the `match` queryset have more than one Individual?
                mci_id = match.first().mci_id
                for filter_name in combo.keys():
                    score += weights[filter_name]
                break

    return mci_id, score
