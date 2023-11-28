
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
    """Calculate the route from origin to destination."""
    try:
        result = gmaps.directions(origin, destination, mode=mode)
        if not result:
            return None, "No route found"
        return result, None
    except Exception as e:
        # Log the error or handle it appropriately
        return None, str(e)

