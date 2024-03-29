
import requests

BIRD_SCOOTER_LOCATION_URL = "https://api.birdapp.com/bird/nearby"
BIRD_CONFIG_URL = "https://api.birdapp.com/config/location"


def request_scooter_location(latitude, longitude, radius):
    headers = {
        'App-Version': '4.41.0',
        'Location': f'{{"latitude":{latitude},"longitude":{longitude},"altitude":500,"accuracy":100,"speed":-1,"heading":-1}}'
    }

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'radius': radius
    }

    try:
        response = requests.get(BIRD_SCOOTER_LOCATION_URL, headers=headers, params=params)
        response.raise_for_status()
        scooter_data = response.json()
        return scooter_data
    except requests.RequestException as e:
        print(f"Error fetching Bird scooter location: {e}")
        return None


def request_configuration(latitude, longitude):
    headers = {
        'App-Version': '4.41.0'
    }

    params = {
        'latitude': latitude,
        'longitude': longitude
    }

    try:
        response = requests.get(BIRD_CONFIG_URL, headers=headers, params=params)
        response.raise_for_status()

        config_data = response.json()
        return config_data
    except requests.RequestException as e:
        print(f"Error fetching Bird configuration: {e}")
        return None


if __name__ == "__main__":
    st_gallen_latitude, st_gallen_longitude = 47.4235, 9.3695
    scooter_data = request_scooter_location(st_gallen_latitude, st_gallen_longitude, radius=1000)

    if scooter_data:
        print("Scooter Data:", scooter_data)

    config_data = request_configuration(st_gallen_latitude, st_gallen_longitude)

    if config_data:
        print("Configuration Data:", config_data)
