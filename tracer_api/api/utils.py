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

def get_city_country(raw_address: str) -> dict[str, str]:

    address = raw_address.split(",")
    _, city = address[1].strip().split(" ")
    return address[2].strip(), city
