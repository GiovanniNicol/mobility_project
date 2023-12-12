# Importing libraries
import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import dateutil
from datetime import datetime

### BACKEND ###
# Creating classes and functions:

## SBB Trains ##
# Creating a class for the SBB train connections
class Connection:
    '''Connection class
       A class that holds information about the transport means (e.g. the trains) and the times of a connection
    '''
    def __init__(self, destination_x, destination_y, departure, arrival, transport_means, departure_platform):
        '''
        Connection constructor
        :param destination_x: the latitude of the destination
        :param destination_y: the longitude of the destination
        :param departure: a string containing the datetime for the departure
        :param arrival: a string containing the datetime for the arrival
        :param transport_means: a list of the transport means of the connection (e.g. ['IC 5'])
        :param departure_platform: the platform number from which the train departs (e.g. ['5'])
        '''

        if (isinstance(destination_x,float) and isinstance(destination_y,float) and
            isinstance(departure,str) and isinstance(arrival,str) and
            isinstance(transport_means,list) and isinstance(departure_platform, str)):
            self.destination_x = destination_x
            self.destination_y = destination_y
            self.transport_means = transport_means
            self.departure_platform = departure_platform

            self.departure_time = dateutil.parser.parse(departure.split('+')[0])
            self.arrival_time = dateutil.parser.parse(arrival.split('+')[0])
        else:
            raise AttributeError

    def __str__(self):
        return "{}: {}->{}".format(self.transport_means, self.departure_platform, self.departure_time, self.arrival_time)

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

# Creating a function to find SBB train connections
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
    departure_platform = first_conn['from']['platform']
  

    return Connection(x, y, departure, arrival, transport_means, departure_platform)

# Function to display SBB train connections
def display_connection(con):
    """
    Displays information about a connection.

    Args:
        con (Connection): The connection to display information about.
    """
    st.markdown(f"### Your next train connection is:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Train Line:**")
        for mean in con.transport_means:
            st.markdown(f"- {mean}")
        st.markdown("**Departure Platform:**")
        st.markdown(f"- {''.join(con.departure_platform)}")
    with col2:
        st.markdown("**Departure:**")
        st.markdown(f"`{con.departure_time.strftime('%d/%m/%Y at %H:%M')}`")
        st.markdown("**Arrival:**")
        st.markdown(f"`{con.arrival_time.strftime('%d/%m/%Y at %H:%M')}`")

# Check what this is
def find_train_connection(origin, destination, departure_date, departure_time):
    try:
        connection = find_connection(origin, destination, departure_date, departure_time)
        display_connection(connection)
    except Exception as e:
        st.error(f"Error finding train connection: {e}")


## Sharedmobility.ch Swiss Federal Office of Energy ##
# Creating a geocoding function which translates addresses into geographic coordinates
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



### FRONTEND ###
## Streamlit App ##

def main():
    # Creating a page header
    st.header('Group 3.4 FS 2023', divider='blue')
    # Creating the title
    st.title("Combined Mobility Finder :world_map:")
    # Creating the subheader
    st.subheader("Hey you, let's look for your SBB train connection ! :blush: :train:")


    # Creating input fields for the SBB train connection with origin, destination, departure date and time
    train_origin = st.text_input("Enter your origin station:")
    train_destination = st.text_input("Enter your destination station:")
    train_departure_date = st.date_input("Enter your departure date:")
    train_departure_time = st.time_input("Enter your departure time:")

    # Creating a button to trigger the train connection search
    if st.button("Find My Train Connection"):
        # Instructing Python to run the find_train_connection function if all information is provided
        if train_origin and train_destination and train_departure_date and train_departure_time:
            try:
                find_train_connection(train_origin, train_destination, train_departure_date, train_departure_time)
            except Exception as e: #Check out what Exception is, is it form the teachers or chat gpt ?
                st.error(f"Error finding train connection: {e}")
        else:
            st.warning("Please fill in all the train connection details.")

    # Creating a second subheader
    st.subheader("Now let's look for shared scooters :scooter:, bikes :bike:, and cars :car: !")

    # Creating an input field for the address
    address = st.text_input("Enter your location address in Switzerland (Street name and number, ZIP Code, City):")

    # Creating a filter button for the different shared mobility vehicle types
    vehicle_types = ['All', 'Car', 'E-Scooter', 'E-CargoBike', 'Bike']
    selected_vehicle_type = st.selectbox("What kind of vehicle do you want?", vehicle_types)

    # Creating a button to trigger the shared mobility search
    if st.button("Find Closest Vehicles"):
        # Telling Python to perform geocoding
        if address:
            coordinates = geocode_address_nominatim(address)

            if coordinates:
                latitude, longitude = coordinates
                tolerance = 200  # You can adjust the tolerance as needed

                # Finding the closest vehicles using the obtained coordinates and the selected vehicle type
                # Telling Python to return the filtered results if the user picks another category than "All"
                if selected_vehicle_type == 'All':
                    result = find_closest_vehicles_all(latitude, longitude, tolerance)
                else:
                    result = find_closest_vehicles_filtered(latitude, longitude, tolerance, selected_vehicle_type)
                

                if result:
                    st.subheader(f"{selected_vehicle_type} vehicles near '{address}':")

                    # Creating a Folium map
                    map_center = (latitude, longitude)
                    my_map = folium.Map(location=map_center, zoom_start=15.5)

                    # Adding a marker for the user-inputted location
                    folium.Marker(map_center, popup="You're Here", icon=folium.Icon(color='red')).add_to(my_map)


                    # Adding markers of different colors for each vehicle type
                    for provider in result:
                        provider_location = (provider['geometry']['y'], provider['geometry']['x'])
                        vehicle_type = provider['attributes']['vehicle_type'][0] if provider['attributes']['vehicle_type'] else 'Unknown'
                        
                        if vehicle_type == 'Car' or vehicle_type == 'E-Car':
                            icon_color = 'orange'
                        elif vehicle_type == 'E-Scooter' or vehicle_type == 'Scooter':
                            icon_color = 'blue'
                        elif vehicle_type == 'E-CargoBike' or vehicle_type == 'Bike':
                            icon_color = 'green'
                        else:
                            icon_color = 'gray'
                            icon = folium.Icon(color='gray')  # Default icon for unknown types

                        folium.Marker(provider_location, popup=f"{vehicle_type.capitalize()} - {provider['attributes']['provider_name']}", icon=folium.Icon(color=icon_color)).add_to(my_map)

                        
                    # Displaying the map using streamlit-folium
                    folium_static(my_map)
            
                # Specifying error messages:
                else:
                    st.warning(f"Sorry, we failed to retrieve vehicle information. There might be no {selected_vehicle_type} vehicle available near you.")
            else:
                st.warning("Geocoding failed.")

if __name__ == "__main__":
    main()

### BIBLIOGRAPHY ###
# Line X to X: Name of the teachers. Year. "Name of the techers vode" from Lecture X Week x. Link on canvas
# Author. (Year). Title of Jupyter Notebook, Week X. Link
# Line X to X
