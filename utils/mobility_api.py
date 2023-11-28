
import requests
from config import MOBILITY_PROVIDER_API_KEY


def get_mobility_service_data(service_url):
    try:
        headers = {'Authorization': f'Bearer {MOBILITY_PROVIDER_API_KEY}'}
        response = requests.get(service_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Log the error, handle it, or pass it up the chain
        print(f"Error fetching data from {service_url}: {e}")
        return None


def get_all_providers_data(providers_info):
    all_data = {}
    for provider_name, provider_details in providers_info.items():
        try:
            data = get_mobility_service_data(provider_details['url'])
            all_data[provider_name] = data
        except Exception as e:
            # Handle or log the error
            all_data[provider_name] = {'error': str(e)}
    return all_data

