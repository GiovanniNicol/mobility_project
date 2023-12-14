# Importing libraries
import googlemaps
import requests
from datetime import datetime
from config import GOOGLE_MAPS_API_KEY

# Defining a function to get an address from the google maps coordinates using the Google Maps API
def get_address_from_coordinates(latitude, longitude):

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    # Specifying the parameters for the API request
    params = {
        "latlng": f"{latitude},{longitude}",
        "key": GOOGLE_MAPS_API_KEY
    }

    # Sending a get request to the Google Maps API
    response = requests.get(url, params=params)

    # Checking whether the get request worked
    if response.status_code == 200:
        results = response.json()["results"]
        # Getting the address components
        if results:
            address_components = results[0]["address_components"]
            street_number = ''
            route = ''
            postal_code = ''
            locality = ''

            # Getting the detailed address (street number, route, postal code and locality) from address_components
            for component in address_components:
                if "street_number" in component["types"]:
                    street_number = component["long_name"]
                elif "route" in component["types"]:
                    route = component["long_name"]
                elif "postal_code" in component["types"]:
                    postal_code = component["long_name"]
                elif "locality" in component["types"]:
                    locality = component["long_name"]

            # Creating a compact address out of the detailed address and returning the compact address
            short_address = f"{route} {street_number}, {postal_code} {locality}"
            return short_address.strip()
            # In case of no result put out "no nearby station found" message
        else:
            return "No nearby station found"
    # Specifying an error message if the API request fails
    else:
        return "Failed to retrieve data from Google Maps API"

# Creating a function to get the google maps coordinates from an address using the Google Maps API (reverse function)
def get_coordinates_from_address(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    # Specifying the parameters for the API request
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }

    # Sending a get request to the Google Maps API
    response = requests.get(url, params=params)

    # Checking whether the get request worked
    if response.status_code == 200:
        results = response.json()["results"]
        if results:
            location = results[0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
        # In case of no result put out "no coordinates found for given address"
        else:
            return "No coordinates found for given address"
    # Specifying an error message if the API request fails
    else:
        return "Failed to retrieve data from Google Maps API"

# Example use
# print(get_coordinates_from_address("Dufourstrasse 50, 9000 St. Gallen"))
# print(get_nearest_station(47.432986, 9.375389))
