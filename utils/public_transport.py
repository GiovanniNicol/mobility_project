
import requests
from datetime import datetime


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
            "arrival_latitude": first_connection["to"]["station"]["coordinate"]["y"],
            "arrival_longitude": first_connection["to"]["station"]["coordinate"]["x"],
            "departure": first_connection["from"]["departure"],
            "arrival": first_connection["to"]["arrival"],
            "transport_means": first_connection["products"]
        }

        return return_object

    else:

        return f"Failed to retrieve data: {response.status_code}"


now = datetime.now()
depart_date = now.strftime("%Y-%m-%d")
depart_time = now.strftime("%H:%M")

print(find_connection("St Gallen", "Zurich", depart_date, depart_time))
