import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import dateutil
from datetime import datetime

# Classes and functions:
class Connection:
    '''Connection class
       A class that holds information about the transport means (e.g. the trains) and the times of a connection
    '''
    def __init__(self, destination_x, destination_y, departure, arrival, transport_means):
        '''
        Connection constructor
        :param destination_x: the latitude of the destination
        :param destination_y: the longitude of the destination
        :param departure: a string containing the datetime for the departure
        :param arrival: a string containing the datetime for the arrival
        :param transport_means: a list of the transport means of the connection (e.g. ['IC 5'])
        '''

        if (isinstance(destination_x,float) and isinstance(destination_y,float) and
            isinstance(departure,str) and isinstance(arrival,str) and
            isinstance(transport_means,list)):
            self.destination_x = destination_x
            self.destination_y = destination_y
            self.transport_means = transport_means

            self.departure_time = dateutil.parser.parse(departure.split('+')[0])
            self.arrival_time = dateutil.parser.parse(arrival.split('+')[0])
        else:
            raise AttributeError

    def __str__(self):
        return "{}: {}->{}".format(self.transport_means, self.departure_time, self.arrival_time)

    def get_unix_departure_time(self):
        '''
        Method get_Unix_departure_time
        Returns the local time of departure as a Unix timestamp
        '''
        return int((self.departure_time - datetime(1970,1,1)).total_seconds())

    def get_unix_arrival_time(self):
        '''
        Method get_Unix_arrival_time
        Returns the local time of arrival as a Unix timestamp
        '''
        return int((self.arrival_time - datetime(1970,1,1)).total_seconds())

# Function to find train connections
def find_connection(origin, destination, departure_date, departure_time):
    url = 'http://transport.opendata.ch/v1/connections'

    params = {}
    params['from'] = origin
    params['to'] = destination
    params['date'] = departure_date
    params['time'] = departure_time

    r = requests.get(url, params = params)
    
    first_conn= r.json()['connections'][0]
    # Uncomment the next line to see the JSON object of first_conn
    # print(json.dumps(first_conn, ensure_ascii=False, indent=4))

    x = first_conn['to']['station']['coordinate']['x']
    y = first_conn['to']['station']['coordinate']['y']
    departure = first_conn['from']['departure']
    arrival = first_conn['to']['arrival']
    transport_means = first_conn['products']

    return Connection(x, y, departure, arrival, transport_means)

# Creating a geocoding function which translates addresses into coordinates (or vice versa?)
def geocode_address_nominatim(address):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            # Take the first result as the most relevant
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            st.error("Geocoding failed. Unable to retrieve location.")
            return None
    else:
        st.error(f"Geocoding failed with status code: {response.status_code}")
        return None

# Creating a function based on the sharedmobility.ch API to retrieve shared mobility vehicles
def find_closest_vehicles_all(latitude, longitude, tolerance):
    url = "https://api.sharedmobility.ch/v1/sharedmobility/identify"
    params = {
        "Geometry": f"{longitude},{latitude}",
        "Tolerance": tolerance,
        "offset": 0,
        "geometryFormat": "esrijson",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Creating a function which allows the user to filter for vehicles type
def find_closest_vehicles_filtered(latitude, longitude, tolerance, selected_vehicle_type):
    all_vehicles = find_closest_vehicles_all(latitude, longitude, tolerance)

    if all_vehicles:
        # Filter vehicles based on the selected vehicle type
        filtered_vehicles = [vehicle for vehicle in all_vehicles if vehicle['attributes']['vehicle_type'] and vehicle['attributes']['vehicle_type'][0] == selected_vehicle_type]
        return filtered_vehicles
    else:
        return None

# Function to display train connections
def display_connection(con):
    """
    Displays information about a connection.

    Args:
        con (Connection): The connection to display information about.
    """
    st.markdown(f"### Connection Found")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Transport Means:**")
        for mean in con.transport_means:
            st.markdown(f"- {mean}")
    with col2:
        st.markdown("**Departure:**")
        st.markdown(f"`{con.departure_time.strftime('%Y-%m-%d %H:%M')}`")
        st.markdown("**Arrival:**")
        st.markdown(f"`{con.arrival_time.strftime('%Y-%m-%d %H:%M')}`")

def find_train_connection(origin, destination, departure_date, departure_time):
    try:
        connection = find_connection(origin, destination, departure_date, departure_time)
        display_connection(connection)
    except Exception as e:
        st.error(f"Error finding train connection: {e}")



# Streamlit app
def main():
    st.title("Combined Mobility Finder")

    # Input fields for the train connection
    train_origin = st.text_input("Train: Enter the origin station:")
    train_destination = st.text_input("Train: Enter the destination station:")
    train_departure_date = st.date_input("Train: Enter the departure date:")
    train_departure_time = st.time_input("Train: Enter the departure time:")

    # Button to trigger the train connection search
    if st.button("Find Train Connection"):
        if train_origin and train_destination and train_departure_date and train_departure_time:
            try:
                find_train_connection(train_origin, train_destination, train_departure_date, train_departure_time)
            except Exception as e:
                st.error(f"Error finding train connection: {e}")
        else:
            st.warning("Please fill in all the train connection details.")

    # Input field for the address
    address = st.text_input("Enter your location address in Switzerland (Street name and number, ZIP Code, City):")

    # Filter button for vehicle types
    vehicle_types = ['All', 'Car', 'E-Scooter', 'E-CargoBike', 'Bike', 'Unknown']
    selected_vehicle_type = st.selectbox("What kind of vehicle do you want?", vehicle_types)

    # Button to trigger the shared mobility search
    if st.button("Find Closest Vehicles"):
        if address:
            # Perform geocoding
            coordinates = geocode_address_nominatim(address)

            if coordinates:
                latitude, longitude = coordinates
                tolerance = 200  # You can adjust the tolerance as needed

                # Find closest vehicles using the obtained coordinates and the selected vehicle type
                if selected_vehicle_type == 'All':
                    result = find_closest_vehicles_all(latitude, longitude, tolerance)
                else:
                    result = find_closest_vehicles_filtered(latitude, longitude, tolerance, selected_vehicle_type)

                if result:
                    st.subheader(f"The closest {selected_vehicle_type} vehicles to the address '{address}' are:")

                    # Create a Folium map
                    map_center = (latitude, longitude)
                    my_map = folium.Map(location=map_center, zoom_start=15.5)

                    # Add marker for the user-inputted location
                    folium.Marker(map_center, popup="You're Here", icon=folium.Icon(color='red')).add_to(my_map)

                    # Creating custom icons
                    bike_icon = folium.CustomIcon(icon_image='bike_icon.png', icon_size=(30, 30))
                    car_icon = folium.CustomIcon(icon_image='car_icon.png', icon_size=(30, 30))
                    scooter_icon = folium.CustomIcon(icon_image='scooter_icon.png', icon_size=(30, 30))

                    # Add markers for each mobility provider with different colors for each type
                    for provider in result:
                        provider_location = (provider['geometry']['y'], provider['geometry']['x'])
                        vehicle_type = provider['attributes']['vehicle_type'][0] if provider['attributes']['vehicle_type'] else 'Unknown'

                        # Set marker color based on vehicle type
                        if vehicle_type == 'Car' or vehicle_type == 'E-Car':
                            icon_color = 'orange'
                            icon = car_icon
                        elif vehicle_type == 'E-Scooter' or vehicle_type == 'Scooter':
                            icon_color = 'blue'
                            icon = scooter_icon
                        elif vehicle_type == 'E-CargoBike' or vehicle_type == 'Bike':
                            icon_color = 'green'
                            icon = bike_icon
                        else:
                            icon_color = 'gray'
                            icon = folium.Icon(color='gray')  # Default icon for unknown types

                        folium.Marker(provider_location, popup=f"{vehicle_type.capitalize()} - {provider['attributes']['provider_name']}", icon=folium.Icon(color=icon_color)).add_to(my_map)

                    # Display the map using streamlit-folium
                    folium_static(my_map)
            

                else:
                    st.warning("Sorry, we failed to retrieve vehicle information. There might be no shared mobilty vehicle available near you.")
            else:
                st.warning("Geocoding failed.")

if __name__ == "__main__":
    main()
