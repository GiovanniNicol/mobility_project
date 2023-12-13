import requests


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
        if data:
            vehicles = []
            for entry in data:
                if 'geometry' in entry and 'x' in entry['geometry'] and 'y' in entry['geometry']:
                    lat = entry['geometry']['y']
                    lng = entry['geometry']['x']
                    vehicles.append((lat, lng))
            return vehicles
    return None

# Example usage
latitude = 47.50024
longitude = 8.72334
tolerance = 200

result = find_closest_vehicles(latitude, longitude, tolerance)
print(result)
