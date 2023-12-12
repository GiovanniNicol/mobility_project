#
# import streamlit as st
# import pandas as pd
# import numpy as np
#
# st.header('FindMyWay :world_map:', divider='blue')
# st.markdown("*Group project 3.4*")
#
# st.subheader('Hey you :blush:')
# st.subheader('Just enter now your location address and the nearest mobility connections will be shown on the map below :arrow_down:')
#
# destination_address = st.text_input("My destination is:")
#
# zurich_coordinates = [47.3769, 8.5417]
#
# df = pd.DataFrame(
#    np.random.randn(700, 2) / [70, 70] +  zurich_coordinates,
#     columns=['lat', 'lon']
# )
#
# st.map(df)

import streamlit as st
from datetime import datetime
from utils import google_maps, public_transport, tier
import pandas as pd
import pydeck as pdk
import geopy.distance


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
st.set_page_config(page_title="Transportation Helper", layout="wide")
st.title("Transportation Helper")

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

        # Prepare a list to hold formatted data for display
        formatted_data = []
        for key, value in filtered_info.items():
            # Format lists into comma-separated strings
            if isinstance(value, list):
                value = ', '.join(value)
            # Format datetime objects into more readable strings
            elif isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            formatted_data.append({'Option': format_key(key), 'Details': value})

        # Display the information in a Pandas DataFrame with improved formatting
        st.subheader("Transport Options")
        df = pd.DataFrame(formatted_data)

        # Use Streamlit's dataframe method to display the DataFrame without the index
        st.dataframe(df, width=700, height=300)  # You can adjust width and height as needed

        # Extract latitude and longitude from connection_info
        latitude = connection_info.get('arrival_latitude')
        longitude = connection_info.get('arrival_longitude')

        if latitude and longitude:
            st.subheader("Train Station Location")

            # Create a DataFrame for pydeck
            train_station_df = pd.DataFrame([{'latitude': latitude, 'longitude': longitude}])

            # Define a pydeck Layer for the train station location
            train_station_layer = pdk.Layer(
                "ScatterplotLayer",
                train_station_df,
                get_position='[longitude, latitude]',
                get_color='[0, 0, 255, 160]',
                get_radius=50,
            )

            # Set the viewport location
            train_station_view_state = pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=14,
                pitch=0,
            )

            # Render the map with pydeck
            train_station_deck = pdk.Deck(layers=[train_station_layer], initial_view_state=train_station_view_state)
            st.pydeck_chart(train_station_deck)


# Additional feature: Find nearby scooters
st.markdown("---")  # Adds a horizontal line for separation
st.subheader("Find Nearby Scooters by Address")

scooter_address = st.text_input("Enter your address to find nearby scooters:")
scooter_radius = st.slider("Radius (in meters)", min_value=100, max_value=1000, value=500, step=50)

if st.button("Find Scooters"):
    scooter_info = tier.get_vehicles_in_range(scooter_address, scooter_radius)
    if scooter_info:
        # Create a DataFrame for pydeck
        scooter_df = pd.DataFrame(scooter_info, columns=['address', 'latitude', 'longitude'])

        # Define a pydeck Layer for scooter locations
        layer = pdk.Layer(
            "ScatterplotLayer",
            scooter_df,
            get_position='[longitude, latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=20,
        )

        # Set the viewport location
        view_state = pdk.ViewState(
            latitude=scooter_df['latitude'].mean(),
            longitude=scooter_df['longitude'].mean(),
            zoom=14,
            pitch=0,
        )

        # Render the map with pydeck
        r = pdk.Deck(layers=[layer], initial_view_state=view_state)
        st.pydeck_chart(r)

        # Input for destination address
        st.subheader("Select a Scooter")
        scooter_selection = st.selectbox("", scooter_df['address'])
        destination_address = st.text_input("Enter your destination address:")

        if scooter_selection and destination_address:
            selected_scooter = scooter_df[scooter_df['address'] == scooter_selection].iloc[0]
            scooter_coords = (selected_scooter['latitude'], selected_scooter['longitude'])
            dest_coords = google_maps.get_coordinates_from_address(destination_address)

            # Calculate distance and time
            distance_km = geopy.distance.distance(scooter_coords, dest_coords).km
            time_hours = distance_km / 16  # Assuming speed is 16 km/h
            st.write(f"Estimated travel time: {time_hours:.2f} hours")

    else:
        st.write("No scooters found or data format is incorrect.")

# you can multiply the walking speed from google maps by the corresponding mode of transport's speed
