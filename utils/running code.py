#Imports #https://docs.python.org/3/library/datetime.html
import requests
from datetime import datetime

#Encapsulating the connection in a class for easier handling #https://www.w3schools.com/python/python_classes.asp
class Connection:
    def __init__(self, x, y, departure, arrival, transport_means):
        self.x = x
        self.y = y
        self.departure = departure
        self.arrival = arrival
        self.transport_means = transport_means


def geocode_address_nominatim(address):
    # Set up the URL for the geocoding service #https://nominatim.org/release-docs/latest/api/Lookup/
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
    }

    # Send a GET request to the geocoding API
    response = requests.get(base_url, params=params)

    # Check if the request was successful (status code 200) #https://www.geeksforgeeks.org/response-methods-python-requests/
    if response.status_code == 200:
        data = response.json()
        if data:
            # Extract latitude and longitude from the first result (most relevant)
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            print("Your address could not be found.")
            return None
    else:
        print(f"Geocoding failed with status code: {response.status_code}")
        return None

def find_closest_vehicles(latitude, longitude, tolerance):
    # Set up the URL for the Shared Mobility API to identify close vehicles #https://github.com/SFOE/sharedmobility/blob/main/Sharedmobility.ch-API.md
    url = "https://api.sharedmobility.ch/v1/sharedmobility/identify"
    params = {
        "Geometry": f"{longitude},{latitude}",
        "Tolerance": tolerance,
        "offset": 0,
        "geometryFormat": "esrijson",
    }

    # Send a GET request to the Shared Mobility API for the location of the vehicles
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200) #https://www.geeksforgeeks.org/response-methods-python-requests/
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def find_connection(origin, destination, departure_date, departure_time):
    # Set up the URL for the Swiss public transportation connections (SBB) API #https://transport.opendata.ch/docs.html#connections
    url = 'http://transport.opendata.ch/v1/connections'

    # Set up parameters for the API request to Swiss public transport connections (SBB) API #https://transport.opendata.ch/docs.html#connections
    params = {}
    params['from'] = origin
    params['to'] = destination
    params['date'] = departure_date
    params['time'] = departure_time

    # Send a GET request to the Swiss public transportation (SBB) API
    r = requests.get(url, params=params)

    # Extract information from the first connection in the response
    first_conn = r.json()['connections'][0]

    # Extract relevant details from the connection data
    x = first_conn['to']['station']['coordinate']['x']
    y = first_conn['to']['station']['coordinate']['y']
    departure = first_conn['from']['departure']
    arrival = first_conn['to']['arrival']
    transport_means = first_conn['products']

    # Create a Connection object with the extracted information
    return Connection(x, y, departure, arrival, transport_means)

# Get user input for the journey details
origin = input("Enter the starting address: ")
destination = input("Enter the destination address: ")
departure_date = input("Enter the departure date (YYYY-MM-DD): ")
departure_time = input("Enter the departure time (HH:MM): ")

# Use geocoding on the start and end address to get latitude and longitude
start_coordinates = geocode_address_nominatim(origin)
end_coordinates = geocode_address_nominatim(destination)

# Check if geocoding was successful for both start and end address
if start_coordinates and end_coordinates:
    start_latitude, start_longitude = start_coordinates
    end_latitude, end_longitude = end_coordinates

    # Find closest vehicles for the current address based on latitude and longitude
    current_address_vehicles = find_closest_vehicles(start_latitude, start_longitude, tolerance=200)

    # Check if vehicle information was successfully retrieved
    if current_address_vehicles:
        print(f"The closest vehicles to your current address ({origin}) are: {current_address_vehicles}")
    else:
        print("Failed to retrieve vehicle information for the current address. There is a chance that no vehicles are in your area.")

    # Find connection using the coordinates and user input
    connection = find_connection(origin, destination, departure_date, departure_time)

    # Check if connection information was successfully retrieved
    if connection:
        print(f"\nThe closest vehicles to the destination address ({destination}) at {departure_time} are:")
        print(f"Departure: {connection.departure}, Arrival: {connection.arrival}")
        print(f"Destination Coordinates: ({connection.x}, {connection.y})")
        print(f"Transport Means: {connection.transport_means}")
    else:
        print("Failed to retrieve connection information.")
else:
    print("Geocoding failed.")

