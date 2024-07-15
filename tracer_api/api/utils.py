""" Helper functions for api application. """

import uuid

def generate_tracking_numbers() -> str:
    """ Generate a unique tracking numbers.
        
    Returns:
        str: A uniquely generated tracking number.
    """

    random_part = uuid.uuid4().hex[:10].upper()
    tracking_number = f'TN{random_part}'
    return tracking_number
