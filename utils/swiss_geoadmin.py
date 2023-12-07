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
        return data
    else:
        return None

# Get user input
latitude = float(input("Enter the latitude: "))
longitude = float(input("Enter the longitude: "))
tolerance = int(input("Enter the tolerance: "))

result = find_closest_vehicles(latitude, longitude, tolerance)
print(result)
