# Importing requests
import requests

# Creating a function to find connections for the public transport
def find_connection(origin, destination, departure_date, departure_time):

    api_url = "http://transport.opendata.ch/v1/connections"

    # Defining parameters origen, destination, departure date and departure time
    params = {
        "from": origin,
        "to": destination,
        "date": departure_date,
        "time": departure_time
    }

    # Usage of the parameters to find a connection in the api_url and storage in response 
    response = requests.get(api_url, params=params)

    if response.status_code == 200:

        data = response.json()

        first_connection = data["connections"][0]

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

        return return_object

    else:

        # Notification in case of failure
        return f"Failed to retrieve data: {response.status_code}"


# now = datetime.now()
# depart_date = now.strftime("%Y-%m-%d")
# depart_time = now.strftime("%H:%M")
#
# nearest_station_result = google_maps.get_address_from_coordinates(47.432986, 9.375389)
# print(find_connection("St Gallen", "Zurich", depart_date, depart_time))
