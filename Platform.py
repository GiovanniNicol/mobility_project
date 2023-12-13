
import streamlit as st
from datetime import datetime
from utils import google_maps, public_transport, tier
import pandas as pd
import pydeck as pdk
import geopy.distance
import math
from geopy.distance import geodesic


def find_transport_options(start, end):
    try:
        now = datetime.now()
        depart_date = now.strftime("%Y-%m-%d")
        depart_time = now.strftime("%H:%M")
        connection_info = public_transport.find_connection(start, end, depart_date, depart_time)
        return connection_info
    except Exception as e:
        st.error(f"Error finding transport options: {e}")
        return None


# Streamlit App Layout
st.set_page_config(page_title="Pocket Travel Aid", layout="wide")
st.title("Pocket Travel Aid")
st.subheader("Public Transport Navigator")
st.markdown("""
This feature helps you navigate the public transport system with ease. Simply enter your start and end addresses 
to find the best route, time, and connection available. 
""")


# Input for manual address entry
# Create a form and use the 'with' statement to wrap the form fields and submit button
with st.form("my_form"):
    # Create columns within the form context
    col1, col2, col3 = st.columns([3, 3, 2])

    with col1:
        start_address = st.text_input("Enter your starting address:")

    with col2:
        end_address = st.text_input("Enter your destination address:")

    # Submit button for the form
    with col3:
        submitted_address = st.form_submit_button("Find Transport Options")


def format_key(key):
    # Replace underscores with spaces and capitalize each word
    return ' '.join(word.capitalize() for word in key.split('_'))


if submitted_address and start_address and end_address:
    connection_info = find_transport_options(start_address, end_address)
    if connection_info:
        # Exclude latitude and longitude from the display
        excluded_keys = ['arrival_latitude', 'arrival_longitude']
        filtered_info = {k: v for k, v in connection_info.items() if k not in excluded_keys}

        # Adding departure and arrival platforms
        filtered_info['departure_platform'] = connection_info.get('departure_platform', 'N/A')
        filtered_info['arrival_platform'] = connection_info.get('arrival_platform', 'N/A')

        # Formatting the data for display
        table_html = "<table style='width:100%'>"
        table_html += "<tr><th>Option</th><th>Details</th></tr>"
        for key, value in filtered_info.items():
            formatted_key = format_key(key)
            if isinstance(value, list):
                formatted_value = ', '.join(value)
            elif isinstance(value, str) and 'T' in value:
                date_part, time_part = value.split('T')
                time_part = time_part.split('+')[0]  # Remove the timezone information
                formatted_value = f"{date_part} at {time_part}"
            else:
                formatted_value = value
            table_html += f"<tr><td>{formatted_key}</td><td>{formatted_value}</td></tr>"
        table_html += "</table>"

        # Display the HTML table without the index
        st.subheader("Information Table")
        st.write(table_html, unsafe_allow_html=True)

        st.write("")

        start_coords = google_maps.get_coordinates_from_address(start_address)
        end_coords = google_maps.get_coordinates_from_address(end_address)

        if start_coords and end_coords and isinstance(start_coords, tuple) and isinstance(end_coords, tuple):
            start_latitude, start_longitude = start_coords
            end_latitude, end_longitude = end_coords

            # Calculate the midpoint for the map
            mid_latitude = (start_latitude + end_latitude) / 2
            mid_longitude = (start_longitude + end_longitude) / 2

            # Determine the differences in latitude and longitude
            lat_diff = abs(start_latitude - end_latitude)
            long_diff = abs(start_longitude - end_longitude)

            # Use the larger difference to adjust the zoom level
            max_diff = max(lat_diff, long_diff)

            # Adjust the zoom level based on the maximum difference
            # This formula is an approximation and might need tweaking
            zoom_level = max(0, min(12, round(8 - math.log(max_diff + 0.1))))

            st.subheader("Connections Map")

            # Create DataFrames for pydeck for both starting and ending locations
            locations_df = pd.DataFrame([
                {'name': 'Start', 'latitude': start_latitude, 'longitude': start_longitude},
                {'name': 'End', 'latitude': end_latitude, 'longitude': end_longitude}
            ])

            # Define pydeck Layers for both locations
            layers = [
                pdk.Layer(
                    "ScatterplotLayer",
                    locations_df[locations_df['name'] == 'Start'],
                    get_position='[longitude, latitude]',
                    get_color='[255, 165, 0, 160]',  # Orange color for start location
                    get_radius=1250,  # Larger radius for start location marker
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    locations_df[locations_df['name'] == 'End'],
                    get_position='[longitude, latitude]',
                    get_color='[0, 128, 0, 160]',  # Green color for end location
                    get_radius=1250,  # Larger radius for end location marker
                )
            ]

            # Set the viewport location to be centered between the start and end locations
            view_state = pdk.ViewState(
                latitude=mid_latitude,
                longitude=mid_longitude,
                zoom=zoom_level,
                pitch=0,
            )

            # Render the map with pydeck using the layers
            deck = pdk.Deck(layers=layers, initial_view_state=view_state)
            st.pydeck_chart(deck)

        else:
            st.error("Could not retrieve coordinates for one or both locations.")

st.write("")

st.subheader("Scooter Locator")
st.markdown("""
Looking for a quick ride? Use the Scooter Locator to find nearby scooters. Enter your address, 
set a search radius, and choose the most convenient scooter for your journey.
""")


# Additional feature: Find nearby scooters
if 'scooter_info' not in st.session_state:
    st.session_state['scooter_info'] = None

with st.form("scooter_form"):
    # Input fields within the form
    scooter_address = st.text_input("Enter your address to find nearby scooters:")
    scooter_radius = st.slider("Radius (in meters)", min_value=100, max_value=2000, value=1000, step=50)

    # Submit button for the form
    find_scooters = st.form_submit_button("Find Scooters")

if find_scooters:
    # Get the scooter info and store it in the session state
    st.session_state['scooter_info'] = tier.get_vehicles_in_range(scooter_address, scooter_radius)

# Retrieve scooter info from session state
scooter_info = st.session_state.get('scooter_info')

if scooter_info:
    # Create DataFrame for pydeck
    scooter_df = pd.DataFrame(scooter_info, columns=['address', 'latitude', 'longitude'])

    # Dropdown to select scooter address
    st.subheader("Select a Scooter")
    selected_scooter_address = st.selectbox("Choose a scooter address:", scooter_df['address'])

    # Create layers for pydeck: one for selected scooter and one for others
    selected_scooter_df = scooter_df[scooter_df['address'] == selected_scooter_address]
    other_scooters_df = scooter_df[scooter_df['address'] != selected_scooter_address]

    layers = [
        # Layer for unselected scooters
        pdk.Layer(
            "ScatterplotLayer",
            other_scooters_df,
            get_position='[longitude, latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=20,
        ),
        # Layer for the selected scooter, highlighted in blue
        pdk.Layer(
            "ScatterplotLayer",
            selected_scooter_df,
            get_position='[longitude, latitude]',
            get_color='[0, 0, 255, 160]',  # Blue color
            get_radius=30,  # Slightly larger to stand out
        ),
    ]

    # Set viewport location for the map
    scooter_view_state = pdk.ViewState(
        latitude=scooter_df['latitude'].mean(),
        longitude=scooter_df['longitude'].mean(),
        zoom=13.5,
        pitch=0,
    )

    # Render the map with pydeck
    scooter_deck = pdk.Deck(layers=layers, initial_view_state=scooter_view_state)
    st.pydeck_chart(scooter_deck)

    # Input for destination address
    st.subheader("Enter Your Destination")

    # Use a form for inputting and submitting the destination address
    with st.form("destination_form"):
        destination_address = st.text_input("Destination address:")
        submit_destination = st.form_submit_button("Submit Destination")

    if submit_destination and destination_address and selected_scooter_address:
        selected_scooter = scooter_df[scooter_df['address'] == selected_scooter_address].iloc[0]
        scooter_coords = (selected_scooter['latitude'], selected_scooter['longitude'])
        dest_coords = google_maps.get_coordinates_from_address(destination_address)

        if dest_coords:
            # Calculate distance and time
            distance_km = geopy.distance.distance(scooter_coords, dest_coords).km
            time_hours = distance_km / 16  # Assuming average scooter speed is 16 km/h

            # Check if travel time is more than 1 hour
            if time_hours > 1:
                st.markdown(
                    "<div style='background-color:#333; color:#fff; padding:10px; border-radius:8px; text-align:center;'>"
                    "You cannot use this mode of transport for such a long distance.</div>",
                    unsafe_allow_html=True)
            else:
                # Styled display of estimated time to match the dark theme
                st.markdown(
                    f"<div style='background-color:#333; color:#fff; padding:10px; border-radius:8px; text-align:center;'>"
                    f"<strong>Estimated Travel Time:</strong> {time_hours:.2f} hours</div>",
                    unsafe_allow_html=True)
        else:
            st.error("Could not retrieve coordinates for the destination address.")

# you can multiply the walking speed from google maps by the corresponding mode of transport's speed
