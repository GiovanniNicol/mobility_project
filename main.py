## SET UP ##
# Run these commands in your terminal before running this code, in case you don't have these libraries installed:
# pip install googlemaps
# pip install geopy

# Importing libraries
import streamlit as st
from datetime import datetime
from utils import google_maps, public_transport, tier
import pandas as pd
import pydeck as pdk
import geopy.distance
import math

# Creating a function to retrieve public transport connection information between two locations for the current date and time
def find_transport_options(start, end):
    try:
        # Getting the current date and time
        now = datetime.now()
        # Formatting the date and the time
        depart_date = now.strftime("%Y-%m-%d")
        depart_time = now.strftime("%H:%M")
        # Calling the function from public_transport to get public transport connections
        connection_info = public_transport.find_connection(start, end, depart_date, depart_time)
        # Returning the obtained connection information
        return connection_info
        
    # Specifying how to handle exceptions and to display an error message with details about the exception
    except Exception as e:
        st.error(f"Error finding transport options: {e}")
        # Returning none
        return None


## STREAMLIT APP ##
# Creating the Streamlit app layout
st.set_page_config(page_title="Pocket Travel Aid", layout="wide")
st.header('Group 3.4 FS 2023', divider='blue')
st.title("Pocket Travel Aid :world_map:")
# Creating a header and description for the Public Transport Navigator
st.subheader("Public Transport Navigator :bus:")
st.markdown("""
This feature helps you navigate the public transport system with ease. Simply enter your start and destination addresses 
to find the best route, time, and connection available. 
""")


# Creating fields for the user to input his starting and destination address (user input form)
with st.form("my_form"):
    col1, col2, spacer, col3 = st.columns([3, 3, 0.1, 2])

    with col1:
        start_address = st.text_input("Enter your starting address:")

    with col2:
        end_address = st.text_input("Enter your destination address:")

    with col3:
        for _ in range(1):
            st.write("")

        # Creating a button to submit all values in the form above
        submitted_address = st.form_submit_button("Find Transport Options")

# Formatting the keys in a more readable way
def format_key(key):
    return ' '.join(word.capitalize() for word in key.split('_'))

# Telling Python to run the function for public transport connection provided that a start and end addresses have been entered and submitted 
if submitted_address and start_address and end_address:
    connection_info = find_transport_options(start_address, end_address)
    
    # Filtering the keys to be displayed
    if connection_info:
        excluded_keys = ['arrival_latitude', 'arrival_longitude']
        filtered_info = {k: v for k, v in connection_info.items() if k not in excluded_keys}
        
        # Adding departure and arrival platform information to the keys to be displayed
        filtered_info['departure_platform'] = connection_info.get('departure_platform', 'N/A')
        filtered_info['arrival_platform'] = connection_info.get('arrival_platform', 'N/A')

        # Creating an HTML table, specifying the header and columns' names
        table_html = "<table style='width:100%'>"
        table_html += "<tr><th>Option</th><th>Details</th></tr>"

        # Formatting the keys for public transport connections in the HTML table
        for key, value in filtered_info.items():
            formatted_key = format_key(key)
            if isinstance(value, list):
                formatted_value = ', '.join(value)
            elif isinstance(value, str) and 'T' in value:
                date_part, time_part = value.split('T')
                time_part = time_part.split('+')[0]
                formatted_value = f"{date_part} at {time_part}"
            else:
                formatted_value = value
            table_html += f"<tr><td>{formatted_key}</td><td>{formatted_value}</td></tr>"
        table_html += "</table>"

        # Displaying the HTML table and adding a header above it
        st.subheader("Route Information")
        st.write(table_html, unsafe_allow_html=True)

        # Inserting a blank space in the app between the Route Information table and the public transport connection map
        st.write("")

        # Retrieving coordinates for start and end addresses using the Google Maps function
        start_coords = google_maps.get_coordinates_from_address(start_address)
        end_coords = google_maps.get_coordinates_from_address(end_address)

        # Telling Python to retrieve latitude and longitude values for start and end locations provided that the start and end coordinates are available and are of tuple type
        if start_coords and end_coords and isinstance(start_coords, tuple) and isinstance(end_coords, tuple):
            start_latitude, start_longitude = start_coords
            end_latitude, end_longitude = end_coords

            # Calculating the midpoint between the start and end coordinates
            mid_latitude = (start_latitude + end_latitude) / 2
            mid_longitude = (start_longitude + end_longitude) / 2

            # Calculating the differences in latitude and longitude
            lat_diff = abs(start_latitude - end_latitude)
            long_diff = abs(start_longitude - end_longitude)
            
            # Determining the maximum difference between latitude and longitude
            max_diff = max(lat_diff, long_diff)

            # Calculating the zoom level for the public transport connection map based on the maximum difference
            zoom_level = max(0, min(12, round(8 - math.log(max_diff + 0.1))))

            # Adding a header for the public transport connection map
            st.subheader("Connections Map")
            
            # Creating a data frame containing the start and end location information
            locations_df = pd.DataFrame([
                {'name': 'Start', 'latitude': start_latitude, 'longitude': start_longitude},
                {'name': 'End', 'latitude': end_latitude, 'longitude': end_longitude}
            ])
            
            # Creating the public transport connection map layers for start and end locations
            layers = [
                pdk.Layer(
                    "ScatterplotLayer",
                    locations_df[locations_df['name'] == 'Start'],
                    get_position='[longitude, latitude]',
                    get_color='[255, 165, 0, 160]',
                    get_radius=1250,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    locations_df[locations_df['name'] == 'End'],
                    get_position='[longitude, latitude]',
                    get_color='[0, 128, 0, 160]',
                    get_radius=1250,
                )
            ]

            # Setting up the initial view state for the public transport connection map
            view_state = pdk.ViewState(
                latitude=mid_latitude,
                longitude=mid_longitude,
                zoom=zoom_level,
                pitch=0,
            )

            # Creating a deck for the public transport connection map deck and displaying the map
            deck = pdk.Deck(layers=layers, initial_view_state=view_state)
            st.pydeck_chart(deck)

        # Specigying an error message if the latitude and longitude values for start and/or end locations cannot be retrieved
        else:
            st.error("Could not retrieve coordinates for one or both locations.")

# Inserting a blank space in the app between the public transport connection map and the Scooter Locator
st.write("")

# Creating a header and description for the Scooter Locator
st.subheader("Scooter Locator :scooter:")
st.markdown("""
Looking for a quick ride? Use the Scooter Locator to find nearby scooters. Enter your address, 
set a search radius, and choose the most convenient scooter for your journey.
""")


# Ensuring that the scooter_info key is available in the session state, and if not set a default value of none
if 'scooter_info' not in st.session_state:
    st.session_state['scooter_info'] = None

# Creating fields for the user to input his location address (user input form), and a slider button to change the radius acceptable to search for scooters
with st.form("scooter_form"):
    scooter_address = st.text_input("Enter your address to find nearby scooters:")
    scooter_radius = st.slider("Radius (in meters)", min_value=100, max_value=2000, value=1000, step=50)

    # Creating a button to submit the values in the form above 
    find_scooters = st.form_submit_button("Find Scooters")

# Telling Python to run the function for finding scooters provided the form above was submitted
if find_scooters:
    st.session_state['scooter_info'] = tier.get_vehicles_in_range(scooter_address, scooter_radius)

# Retrieving the scooter info from session state
scooter_info = st.session_state.get('scooter_info')

# Creating a data frame with scooter info provided it is available
if scooter_info:
    scooter_df = pd.DataFrame(scooter_info, columns=['address', 'latitude', 'longitude'])

    # Creating a header to select a scooter
    st.subheader("Select a Scooter")
    # Creating a dropdown button to select a scooter address among the returned scooters
    selected_scooter_address = st.selectbox("Choose a scooter address:", scooter_df['address'])

    # Separating the selected scooter from the other scooters for the map display
    selected_scooter_df = scooter_df[scooter_df['address'] == selected_scooter_address]
    other_scooters_df = scooter_df[scooter_df['address'] != selected_scooter_address]

    # Creating the scooter map layers for the selected scooter and the other scooters
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            other_scooters_df,
            get_position='[longitude, latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=20,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            selected_scooter_df,
            get_position='[longitude, latitude]',
            get_color='[0, 0, 255, 160]',
            get_radius=30,
        ),
    ]

    # Setting up the initial view state for the scooter map
    scooter_view_state = pdk.ViewState(
        latitude=scooter_df['latitude'].mean(),
        longitude=scooter_df['longitude'].mean(),
        zoom=13.5,
        pitch=0,
    )

    # Creating a deck for the scooter map deck and displaying the map
    scooter_deck = pdk.Deck(layers=layers, initial_view_state=scooter_view_state)
    st.pydeck_chart(scooter_deck)

    # Creating an information field to indicate where the selected scooter is located on the map
    if selected_scooter_address:
        st.info(
            f"The blue dot on the map indicates the approximate location of the selected scooter "
            f"at: {selected_scooter_address}")

    # Creating a header for the journey calculation feature
    st.subheader("Enter Your Destination")

    # Creating fields for the user to input his destination address (user input form)
    with st.form("destination_form"):
        destination_address = st.text_input("Destination address:")
        # Creating a button to submit the values in the form above
        submit_destination = st.form_submit_button("Submit Destination")

    # Telling Python to retrieve the coordinates of the selected scooter and of the destination address provided that a scooter address has been selected, and a destination address has been entered and submitted
    if submit_destination and destination_address and selected_scooter_address:
        selected_scooter = scooter_df[scooter_df['address'] == selected_scooter_address].iloc[0]
        scooter_coords = (selected_scooter['latitude'], selected_scooter['longitude'])
        dest_coords = google_maps.get_coordinates_from_address(destination_address)

        # Calculating distance between scooter location and destination location, and calculating the the estimated travel time
        if dest_coords:
            distance_km = geopy.distance.distance(scooter_coords, dest_coords).km
            time_hours = distance_km / 16 # We assume a scooter speed of 16 km/h

            # Separating the estimated travel time in hours and minutes
            hours = int(time_hours)
            minutes = int((time_hours - hours) * 60)

            # Telling Python to display a message 
            # When the estimated travel time is greater than 2 hours
            if time_hours > 2:
                st.markdown(
                    "<div style='background-color:#333; color:#fff; padding:10px; border-radius:8px; text-align:center;'>"
                    "You cannot use this mode of transport for such a long distance.</div>",
                    unsafe_allow_html=True)
                
            # and otherwise if the travel time is under 2 hours, to display the estimated travel time 
            else:
                time_display = f"{hours} hour{'s' if hours > 2 else ''} {minutes} minutes"
                st.markdown(
                    f"<div style='background-color:#f0f0f0; color:#333; padding:10px; border-radius:8px; text-align:center;'>"
                    f"<strong>Estimated Travel Time:</strong> {time_display}</div>",
                    unsafe_allow_html=True)
        
        # Displaying an error message if the coordinates for the destination address could not be retrieved
        else:
            st.error("Sorry, we could not retrieve coordinates for the destination address.")

# Displaying an error message if the function could not find any scooter at the user's location address within the specified radius
else:
    st.warning(f"Sorry, we failed to find any scooter nearby. You may need to increase the radius.")

## SOURCES ##
# ChatGPT for creating the public transport connection map with a pydeck map (lines 116-128 and 133-171) and for creating the scooter map (lines 212 to 244)
