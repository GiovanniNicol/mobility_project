import requests
from config import GOOGLE_MAPS_API_KEY


def get_address_from_coordinates(latitude, longitude):

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "latlng": f"{latitude},{longitude}",
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()["results"]
        if results:
            address_components = results[0]["address_components"]
            street_number = ''
            route = ''
            postal_code = ''
            locality = ''

            for component in address_components:
                if "street_number" in component["types"]:
                    street_number = component["long_name"]
                elif "route" in component["types"]:
                    route = component["long_name"]
                elif "postal_code" in component["types"]:
                    postal_code = component["long_name"]
                elif "locality" in component["types"]:
                    locality = component["long_name"]

            short_address = f"{route} {street_number}, {postal_code} {locality}"
            return short_address.strip()
        else:
            return "No nearby station found"
    else:
        return "Failed to retrieve data from Google Maps API"


def get_coordinates_from_address(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()["results"]
        if results:
            location = results[0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
        else:
            return "No coordinates found for given address"
    else:
        return "Failed to retrieve data from Google Maps API"

# print(get_coordinates_from_address("Dufourstrasse 50, 9000 St. Gallen"))
# print(get_nearest_station(47.432986, 9.375389))
