from matching.database import engine, individual, session

def compute_score(weights: dict):
    score = 0.0
    for weight in weights.keys():
        score += weights[weight]
    return score

def compute_mci_threshold(individual_args: dict):
    """Compute the MCI Threshold for a given individual.
    Notes:
        For the purpose of this exercise, we estimate our probability to be:
            first_name * last_name * email_address * address * dob * ssn
    """

    match = None
    score = 0.0

    potential_matches = session.query(individual).filter_by(
        first_name=individual_args['first_name'],
        date_of_birth=individual_args['date_of_birth'],
    )

    if potential_matches:
        score = 0.4

        filters = {
            'last_name': individual_args.get('last_name', None),
            'telephone': individual_args.get('telephone', None),
            'gender_id': individual_args.get('gender', None),
            'email_address': individual_args.get('email', None),
            'mailing_address_id': individual_args.get('mailing_address_id', None),
            'ssn': individual_args.get('ssn'),
        }

        import pdb; pdb.set_trace()
        more_potential_matches = potential_matches.filter_by(**filters).all()

        if len(more_potential_matches) == 1:
            # Perfect match!
            score += 0.6
            match = more_potential_matches.first()
        elif len(more_potential_matches) > 1:
            # Too many matches returned. 
            # Not enough data to determine a match.
            match = None
        else:
            # thanks itertools! 
            # https://stackoverflow.com/questions/11905573/getting-all-combinations-of-key-value-pairs-in-python-dict
            from itertools import combinations
            filter_combinations = list(map(dict, combinations(filters.items(), 5)))

            for filter_c in filter_combinations:
                match = potential_matches.filter_by(filter_c)

                if match:
                    score += 0.5
        
    return match, score



    weights = {
        'first_name': 0.1,
        'last_name': 0.1,
        'mailing_address_id': 0.2,
        'date_of_birth': 0.2,
        'ssn': 0.4
    }

    filters = {
        'first_name': individual_args.get('first_name', None),
        'last_name': individual_args.get('last_name', None),
        'mailing_address_id': individual_args.get('mailing_address_id', None),
        'date_of_birth': individual_args.get('date_of_birth', None),
        'ssn': individual_args.get('ssn', None),
    }

    while not matched and len(filters.keys()) > 0:
        match = session.query(individual).filter_by(**filters).first()
        if match:
            matched = True
            score = compute_score(weights)
        else:
            for key in weights.keys():
                del(weights[key])
                del(filters[key])
                break

    return match, score
