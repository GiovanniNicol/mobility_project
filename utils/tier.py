# Importing libraries
import requests
from config import TIER_API_KEY
from utils import google_maps

# Defining the API-key (from tier) and the base-URL
base_url = "https://platform.tier-services.io"

headers = {
    "X-Api-Key": TIER_API_KEY
}

# Creating a function that calls the coordintes from the address by using the get_coordinates_from_address function from google_maps
def get_coordinates_from_address(address):
    return google_maps.get_coordinates_from_address(address)

# Creating a function to find vehicles that are in a specific radius around the address
def get_vehicles_in_range(address, rad):
    lat, lng = get_coordinates_from_address(address)
    url = f"{base_url}/v1/vehicle"

    # Defining the parameters latitude, longitude and radius
    params = {
        "lat": lat,
        "lng": lng,
        "radius": rad,
    }

    # Sending a get request to the Tier API
    r = requests.get(url, headers=headers, params=params)

    # Checking whether the get request worked
    if r.status_code == 200:

        data = r.json()["data"]

        # Creating an empty list to store the scooter information
        output = []

        for i in data:
            # Telling Python to check whether the vehicle is an electric scooter with a non-zero battery level and is rentable
            if i["attributes"]["vehicleType"] == "escooter" and i["attributes"]["batteryLevel"] > 0 \
                    and i["attributes"]["isRentable"] == True:
                # Getting the latitude and longitude of the scooter
                lat = i["attributes"]["lat"]
                lng = i["attributes"]["lng"]
                # Match the scooter's coordinates to a Google Maps address
                new_address = google_maps.get_address_from_coordinates(lat, lng)
                # Getting the maximum speed of the scooter
                speed = i["attributes"]["maxSpeed"]
                # Appending the scooter information to the output list
                output.append((new_address, lat, lng))

        return output

    else:
        # Specifying an error message if the API request fails
        return f"Failed to retrieve data: {r.status_code}"

# Example use
address = "Dufourstrasse 50, 9000 St. Gallen"
radius = 500

# print(get_vehicles_in_range(address, radius))
