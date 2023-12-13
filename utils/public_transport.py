import requests
from datetime import datetime
from utils import google_maps


def find_connection(origin, destination, departure_date, departure_time):

    api_url = "http://transport.opendata.ch/v1/connections"

    params = {
        "from": origin,
        "to": destination,
        "date": departure_date,
        "time": departure_time
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:

        data = response.json()

        first_connection = data["connections"][0]

        return_object = {
            "arrival_latitude": first_connection["to"]["station"]["coordinate"]["x"],
            # the mobility provider mixed up y with x
            "arrival_longitude": first_connection["to"]["station"]["coordinate"]["y"],
            # the mobility provider mixed up x with y
            "departure": first_connection["from"]["departure"],
            "arrival": first_connection["to"]["arrival"],
            "transport_means": first_connection["products"],
            "departure_platform": first_connection["from"]["platform"],
            "arrival_platform": first_connection["to"]["platform"]
        }

        return return_object

    else:

        return f"Failed to retrieve data: {response.status_code}"


now = datetime.now()
depart_date = now.strftime("%Y-%m-%d")
depart_time = now.strftime("%H:%M")

nearest_station_result = google_maps.get_address_from_coordinates(47.432986, 9.375389)
# print(find_connection("St Gallen", "Zurich", depart_date, depart_time))
