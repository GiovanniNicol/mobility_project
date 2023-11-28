
import googlemaps
from config import GOOGLE_MAPS_API_KEY

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


def get_geocode(address):
    """Get the geocode for a given address."""
    try:
        result = gmaps.geocode(address)
        if not result:
            return None, "No results found"
        return result, None
    except Exception as e:
        # Log the error or handle it appropriately
        return None, str(e)


def calculate_route(origin, destination, mode='driving'):
    try:
        directions_result = gmaps.directions(origin, destination, mode=mode)
        if not directions_result:
            return None, "No route found"

        # Extract distance and duration
        route = directions_result[0]['legs'][0]
        distance = route['distance']['text']
        duration = route['duration']['text']

        return {'distance': distance, 'duration': duration, 'route': directions_result}, None
    except Exception as e:
        # Improved error logging
        return None, f"Error calculating route: {e}"
