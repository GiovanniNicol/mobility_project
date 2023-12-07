import requests
from datetime import datetime

class Connection:
    def __init__(self, x, y, departure, arrival, transport_means):
        self.x = x
        self.y = y
        self.departure = departure
        self.arrival = arrival
        self.transport_means = transport_means

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

def find_connection(origin, destination, departure_date, departure_time):
    url = 'http://transport.opendata.ch/v1/connections'

    params = {}
    params['from'] = origin
    params['to'] = destination
    params['date'] = departure_date
    params['time'] = departure_time

    r = requests.get(url, params=params)

    first_conn = r.json()['connections'][0]
    # Uncomment the next line to see the JSON object of first_conn
    # print(json.dumps(first_conn, ensure_ascii=False, indent=4))

    x = first_conn['to']['station']['coordinate']['x']
    y = first_conn['to']['station']['coordinate']['y']
    departure = first_conn['from']['departure']
    arrival = first_conn['to']['arrival']
    transport_means = first_conn['products']

    return Connection(x, y, departure, arrival, transport_means)

# Get user input for the journey details
origin = input("Enter the starting address: ")
destination = input("Enter the destination address: ")
departure_date = input("Enter the departure date (YYYY-MM-DD): ")
departure_time = input("Enter the departure time (HH:MM): ")

# Perform geocoding for the start and end points
start_coordinates = geocode_address_nominatim(origin)
end_coordinates = geocode_address_nominatim(destination)

if start_coordinates and end_coordinates:
    start_latitude, start_longitude = start_coordinates
    end_latitude, end_longitude = end_coordinates

    # Find closest vehicles for the current address
    current_address_vehicles = find_closest_vehicles(start_latitude, start_longitude, tolerance=200)

    if current_address_vehicles:
        print(f"The closest vehicles to your current address ({origin}) are: {current_address_vehicles}")
    else:
        print("Failed to retrieve vehicle information for the current address.")

    # Find connection using the obtained coordinates and user input
    connection = find_connection(origin, destination, departure_date, departure_time)

    if connection:
        print(f"\nThe closest vehicles to the destination address ({destination}) at {departure_time} are:")
        print(f"Departure: {connection.departure}, Arrival: {connection.arrival}")
        print(f"Destination Coordinates: ({connection.x}, {connection.y})")
        print(f"Transport Means: {connection.transport_means}")
    else:
        print("Failed to retrieve connection information.")
else:
    print("Geocoding failed.")
