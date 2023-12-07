import requests

def geocode_address_nominatim(address):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            # Take the first result as the most relevant
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            print("Geocoding failed. Unable to retrieve location.")
            return None
    else:
        print(f"Geocoding failed with status code: {response.status_code}")
        return None

def find_closest_vehicles(latitude, longitude, tolerance):
    url = "https://api.sharedmobility.ch/v1/sharedmobility/identify"
    params = {
        "Geometry": f"{longitude},{latitude}",
        "Tolerance": tolerance,
        "offset": 0,
        "geometryFormat": "esrijson",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Get user input for the address
address = input("Enter the address in Switzerland: ")

# Perform geocoding
coordinates = geocode_address_nominatim(address)

if coordinates:
    latitude, longitude = coordinates
    tolerance = 200  # You can adjust the tolerance as needed

    # Find closest vehicles using the obtained coordinates
    result = find_closest_vehicles(latitude, longitude, tolerance)

    if result:
        print(f"The closest vehicles to the address '{address}' are: {result}")
    else:
        print("Failed to retrieve vehicle information.")
else:
    print("Geocoding failed.")

