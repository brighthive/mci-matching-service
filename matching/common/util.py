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
    matched = False
    score = 0.0

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