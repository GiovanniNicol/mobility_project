import requests
from config import TIER_API_KEY

base_url = "https://platform.tier-services.io"

headers = {
    "X-Api-Key": TIER_API_KEY
}


def get_vehicles_in_range(lat, long, rad):
    url = f"{base_url}/v1/vehicle"

    params = {
        "lat": lat,
        "lng": long,
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
                speed = i["attributes"]["maxSpeed"]
                output.append((lat, lng, speed * 0.8))
                # I multiply by 0.8 indicating the efficiency of using the max speed of the escooter
                # (user likely only to use 80% of the max speed by assumption)

        return output

    else:

        return f"Failed to retrieve data: {r.status_code}"


latitude = 48.1
longitude = 16.3
radius = 2000

print(get_vehicles_in_range(latitude, longitude, radius))
