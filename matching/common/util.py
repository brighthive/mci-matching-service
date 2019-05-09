from itertools import combinations

from matching.database import engine, individual, session

def compute_match_with_score(individual_args: dict):
    """
    This function determines if incoming data for an Individual
    can be reasonably matched with an existing entry. 

    A match can have a score of 1.0, i.e., an existing entry meets the conditions 
    described by the incoming Individual data (see: `filters` below). 

    Or a match can have a score of 0.9, i.e., an existing entry matches
    the `first_name` and `date_of_birth`, as well as five other fields, of the incoming Individual.

    Implicit in this logic: the `first_name` and `last_name` are weighted at 0.2 (or 0.4 together)
    and each remaining field are weighted at 0.1. Note! The precise weights for these fields
    will be fine tuned, as we come to understand the data better.

    :param individual_args: a dict of Individual data that includes, at minimum, a
    `first_name` and `date_of_birth`.

    :returns: an Individual and a score of the match likelihood (or None) 
    """

    mci_id = None
    score = None
    
    
    ssn = individual_args.get('ssn')
    if ssn: 
        ssn_last_four_digits = ssn[-4:]

    filters = {
        'last_name': individual_args.get('last_name'),
        'telephone': individual_args.get('telephone'),
        'gender_id': individual_args.get('gender_id'),
        'email_address': individual_args.get('email_address'),
        'mailing_address_id': individual_args.get('mailing_address_id'),
        'ssn': individual_args.get('ssn'),
        # 'ssn': like("%s{}".format(ssn_last_four_digits)) if ssn_last_four_digits else ssn,
        # TODO: how to query for last four digits of SSN, and move the logic further upstream
    }


    exact_match = session.query(individual).filter_by(
        first_name=individual_args['first_name'],
        date_of_birth=individual_args['date_of_birth']
    ).filter_by(**filters)

    if exact_match.first():
        # Note: the sample data has duplicates (e.g., Susan Hall)
        # So, an exact_match queryset can contain more than one entry.
        # Is it better to just match with one? rather than create a third duplicate?
        mci_id = exact_match.first().mci_id
        score = 1.0
    else:
        # thanks itertools! 
        # https://stackoverflow.com/questions/11905573/getting-all-combinations-of-key-value-pairs-in-python-dict
        filter_combinations = list(map(dict, combinations(filters.items(), 5)))
        import pdb; pdb.set_trace()

        for filter_combo in filter_combinations:
            strong_match = session.query(individual).filter_by(
                first_name=individual_args['first_name'],
                date_of_birth=individual_args['date_of_birth'],
            ).filter_by(**filter_combo)

            if strong_match.first():
                # TO TEST can strong_match have more than one object?
                mci_id = strong_match.first().mci_id
                score = 0.9
                break
        
    return mci_id, score
