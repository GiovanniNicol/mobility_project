
from flask import Flask, jsonify
from utils.google_maps import get_geocode, calculate_route
from utils.mobility_api import get_mobility_service_data

app = Flask(__name__)


@app.route('/')
def index():
    # This is the main route, which could return a simple message
    # or serve an HTML file if you're planning to have a frontend
    return "Welcome to the Mobility App!"


@app.route('/geocode/<address>')
def geocode(address):
    # Replace 'address' with the actual address string passed in the URL
    geocode_result = get_geocode(address)
    return jsonify(geocode_result)


@app.route('/route/<origin>/<destination>')
def route(origin, destination):
    # Replace 'origin' and 'destination' with actual locations passed in the URL
    route_result = calculate_route(origin, destination)
    return jsonify(route_result)


@app.route('/mobility_services')
def mobility_services():
    # Fetch data from all mobility service providers and return as JSON
    services_data = get_mobility_service_data()
    return jsonify(services_data)


if __name__ == '__main__':
    app.run(debug=True)

