# Importing libraries
import requests
from datetime import datetime
from utils import google_maps

# Creating a function to find public transport connections
def find_connection(origin, destination, departure_date, departure_time):

    # SBB public transport API url
    api_url = "http://transport.opendata.ch/v1/connections"

    # Scpecifying the parameters for the API request (origin, destination, departure date, and departure time)
    params = {
        "from": origin,
        "to": destination,
        "date": departure_date,
        "time": departure_time
    }

    # Sending a get request to the SBB public transport API url
    response = requests.get(api_url, params=params)

    # Checking whether the get request worked
    if response.status_code == 200:

        data = response.json()

        # Getting the information from the first connection in the response
        first_connection = data["connections"][0]

        # Creating a dictionary containing the relevant connection details (latitude, longitude, departure time and platform, arrival time and platform, transport means (public transport lines))
        return_object = {
            "arrival_latitude": first_connection["to"]["station"]["coordinate"]["x"],
            # the mobility provider mixed up y with x
            "arrival_longitude": first_connection["to"]["station"]["coordinate"]["y"],
            # the mobility provider mixed up x with y
            "departure_time": first_connection["from"]["departure"],
            "departure_platform": first_connection["from"]["platform"],
            "arrival_time": first_connection["to"]["arrival"],
            "arrival_platform": first_connection["to"]["platform"],
            "transport_means": first_connection["products"],
        }

        # Returning the connection details
        return return_object

    else:

        # Specifying an error message if the get request failed
        return f"Failed to retrieve data: {response.status_code}"

# Getting the current date and time
now = datetime.now()
depart_date = now.strftime("%Y-%m-%d")
depart_time = now.strftime("%H:%M")

# Example use
# nearest_station_result = google_maps.get_address_from_coordinates(47.432986, 9.375389)
# print(find_connection("St Gallen", "Zurich", depart_date, depart_time))
