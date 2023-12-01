import requests

def get_closest_vehicle(location):
    # Step 1: Use GeoAdmin API to get coordinates of the input location
    geoadmin_api_url = "https://api3.geo.admin.ch/services/sdiservices/search"
    geoadmin_params = {
        "query": location,
        "layer": "ch.bfe.sharedmobility.station",
        "time": "2022-01-01",  # You can adjust the time parameter if needed
    }

    geoadmin_response = requests.get(geoadmin_api_url, params=geoadmin_params)
    geoadmin_data = geoadmin_response.json()

    # Check if coordinates are available
    if "features" not in geoadmin_data or not geoadmin_data["features"]:
        return "Coordinates not found for the provided location."

    # Extract coordinates from GeoAdmin response
    coordinates = geoadmin_data["features"][0]["geometry"]["coordinates"]
    latitude, longitude = coordinates[1], coordinates[0]

    # Step 2: Use sharedmobility.ch API to get the closest vehicle
    sharedmobility_api_url = "https://api.sharedmobility.ch/v1/sharedmobility/identify"
    sharedmobility_params = {
        "Geometry": f"{longitude},{latitude}",
        "Tolerance": 500,  # You can adjust the tolerance parameter if needed
        "offset": 0,
        "geometryFormat": "esrijson",
    }

    sharedmobility_response = requests.get(sharedmobility_api_url, params=sharedmobility_params)
    sharedmobility_data = sharedmobility_response.json()

    # Check if vehicles are available
    if "features" not in sharedmobility_data or not sharedmobility_data["features"]:
        return "No vehicles found near the provided location."

    # Extract information about the closest vehicle
    closest_vehicle = sharedmobility_data["features"][0]
    vehicle_type = closest_vehicle["attributes"]["ch.bfe.sharedmobility.vehicle_type"]
    provider_id = closest_vehicle["attributes"]["ch.bfe.sharedmobility.provider.id"]

    return f"The closest {vehicle_type} from provider {provider_id} is located at {latitude}, {longitude}."

# Example usage
user_input_location = input("Enter the location: ")
result = get_closest_vehicle(user_input_location)
print(result)


