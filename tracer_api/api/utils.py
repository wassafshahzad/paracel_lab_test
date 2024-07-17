""" Helper functions for api application. """

import uuid
import requests
import pycountry
import os
from typing import Any, Callable

from django.http import Http404
from django.core.cache import cache
from rest_framework.exceptions import APIException

from api.constants import WEATHER_API


def generate_tracking_numbers() -> str:
    """Generate a unique tracking numbers.

    Returns:
        str: A uniquely generated tracking number.
    """

    random_part = uuid.uuid4().hex[:10].upper()
    tracking_number = f"TN{random_part}"
    return tracking_number


def get_postal_city_country(raw_address: str) -> tuple[str, str, str]:
    """Get country, city and postal code from raw address.

    Args:
        raw_address (str): String of raw address.

    Returns:
        tuple[str, str, str]: Dict of postal code, country and city.
    """

    address = raw_address.split(",")
    postal_code, city = address[1].strip().split(" ")
    country = address[2].strip()
    return postal_code, country, city


def get_weather_data(postal_code: str, country: str) -> dict[str, Any]:
    """Get data from weather API.

    Args:
        postal_code: Postal Code of location.
        country: Country of location.

    Raises:
        Http404: _description_
        APIException: _description_

    Returns:
        dict[str, Any]: The response data.
    """

    try:
        country_code = pycountry.countries.lookup(country).alpha_2
    except LookupError:
        raise Http404("Country not found")

    data = requests.get(
        WEATHER_API.format(
            postal_code=postal_code,
            country_code=country_code,
            API_KEY=os.environ.get("API_KEY"),
        )
    )
    if not data.ok:
        raise APIException(code=400, detail="Error Occurred with the weather API.")
    return data.json()


def get_cached_weather_data(key: str) -> dict[str, Any]:
    """Get cached data weather data and set it if not found.

    Args:
        key: Key of the cache data
    """
    data = cache.get(key, None)
    postal_code, country = key.split("_")

    print("Getting data from Cache.")

    if not data:
        print("Getting data from API.")
        data = get_weather_data(postal_code, country)["data"][0]
        data = {"temp": data.get("temp", ""), "weather": data.get("weather", "")}
        cache.set(
            key,
            data,
        )
    return data

