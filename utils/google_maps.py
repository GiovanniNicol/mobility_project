# importing google maps api
import requests
from config import GOOGLE_MAPS_API_KEY

# defining a function get the address from the google maps coordinates
def get_address_from_coordinates(latitude, longitude):

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    # using the parameters to get the coordinates and storing the address in response
    params = {
        "latlng": f"{latitude},{longitude}",
        "key": GOOGLE_MAPS_API_KEY
    }

    # requesting the google maps url with help of the parameters and convert responses as strings
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()["results"]
        if results:
            address_components = results[0]["address_components"]
            street_number = ''
            route = ''
            postal_code = ''
            locality = ''

            # getting the detailed address (street number, route, postal code and locality) from address_components
            for component in address_components:
                if "street_number" in component["types"]:
                    street_number = component["long_name"]
                elif "route" in component["types"]:
                    route = component["long_name"]
                elif "postal_code" in component["types"]:
                    postal_code = component["long_name"]
                elif "locality" in component["types"]:
                    locality = component["long_name"]

            # getting the compact address out of the detailed address and return compact address
            short_address = f"{route} {street_number}, {postal_code} {locality}"
            return short_address.strip()
            # in case of no result put out "no nearby station found"
        else:
            return "No nearby station found"
    # in case of failure   
    else:
        return "Failed to retrieve data from Google Maps API"

# creating a function to get cordinates from address
def get_coordinates_from_address(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    # using the parameters address and the google maps api key
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }

    # requesting the google maps api and returning the latitude and length as response
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()["results"]
        if results:
            location = results[0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
        # in case of no result put out "no coordinates found for given address"
        else:
            return "No coordinates found for given address"
    # in case of failure 
    else:
        return "Failed to retrieve data from Google Maps API"

# print(get_coordinates_from_address("Dufourstrasse 50, 9000 St. Gallen"))
# print(get_nearest_station(47.432986, 9.375389))
