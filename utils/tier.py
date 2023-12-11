# Step 1: importing libraries

import requests

import config
from config import TIER_API_KEY

# set the base URL for Tier API
base_url = "https://platform.tier-services.io"

# set headers with the required API key
headers = {
    "X-API-Key": config.TIER_API_KEY,
}


# Function for getting vehicles within range
def get_vehicles_in_range(lat, lng, radius):
    endpoint = f"{base_url}/v1/vehicle"
    params = {
        "lat": lat,
        "lng": lng,
        "radius": radius,
    }
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()


# Function for requesting Scooter Location:

def request_scooter_location(api_key, longitude, latitude, radius):
    # Set the base URL for Tier API
    base_url = "https://platform.tier-services.io"

    # Set headers with the required API key
    headers = {
        "X-Api-Key": api_key,
    }

    # Construct parameters for the request
    params = {
        "lng": longitude,
        "lat": latitude,
        "radius": radius,
    }

    # Endpoint for getting vehicles within a range
    endpoint = f"{base_url}/v1/vehicle"

    # Send GET request to the API
    response = requests.get(endpoint, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return JSON data
        return response.json()
    else:
        # Return nothing if the request was not successful
        print(f"Failed to retrieve scooter location. Status code: {response.status_code}")
        return None


# Example usage:
# Replace with your actual API key, longitude, latitude, and radius
api_key = "bpEUTJEBTf74oGRWxaIcW7aeZMzDDODe1yBoSxi2"
longitude = 16.3
latitude = 48.1
radius = 5000

# Call the function
scooter_location_data = request_scooter_location(api_key, longitude, latitude, radius)

# Handle the response as needed in your application
if scooter_location_data:
    print("Scooter Location Data:", scooter_location_data)
else:
    print("No scooter location data available.")


# Set up function to request Configuration:

def request_configuration(api_key, latitude, longitude):
    # Set the base URL for Tier API
    base_url = "https://platform.tier-services.io"

    # Set headers with the required API key
    headers = {
        "X-Api-Key": api_key,
    }

    # Construct parameters for the request
    params = {
        "lat": latitude,
        "lng": longitude,
    }

    # Endpoint for getting configuration
    endpoint = f"{base_url}/v1/configuration"

    # Send GET request to the API
    response = requests.get(endpoint, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return JSON data
        return response.json()
    else:
        # Return nothing if the request was not successful
        print(f"Failed to retrieve configuration. Status code: {response.status_code}")
        return None


# Example usage:
# Replace with your actual API key, latitude, and longitude
api_key = "bpEUTJEBTf74oGRWxaIcW7aeZMzDDODe1yBoSxi2"
latitude = 48.1
longitude = 16.3

# Call the function
configuration_data = request_configuration(api_key, latitude, longitude)

# Handle the response as needed in your application
if configuration_data:
    print("Configuration Data:", configuration_data)
else:
    print("No configuration data available.")
