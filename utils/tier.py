import requests
from config import TIER_API_KEY
from utils import google_maps

base_url = "https://platform.tier-services.io"

headers = {
    "X-Api-Key": TIER_API_KEY
}


def get_coordinates_from_address(address):
    return google_maps.get_coordinates_from_address(address)


def get_vehicles_in_range(address, rad):
    lat, lng = get_coordinates_from_address(address)
    url = f"{base_url}/v1/vehicle"

    params = {
        "lat": lat,
        "lng": lng,
        "radius": rad,
    }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code == 200:

        data = r.json()["data"]

        output = []

        for i in data:
            if i["attributes"]["vehicleType"] == "escooter" and i["attributes"]["batteryLevel"] > 0 \
                    and i["attributes"]["isRentable"] == True:
                lat = i["attributes"]["lat"]
                lng = i["attributes"]["lng"]
                new_address = google_maps.get_address_from_coordinates(lat, lng)
                output.append((new_address, lat, lng))

        return output

    else:

        return f"Failed to retrieve data: {r.status_code}"


address = "Dufourstrasse 50, 9000 St. Gallen"
radius = 500

# print(get_vehicles_in_range(address, radius))
