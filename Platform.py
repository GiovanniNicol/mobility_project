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
        return public_transport.find_connection(start, end, depart_date, depart_time)
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
        filtered_info = {format_key(k): v for k, v in connection_info.items() if k not in excluded_keys}

        # Format date-time strings
        for key, value in filtered_info.items():
            if isinstance(value, str) and "T" in value:
                filtered_info[key] = value.replace("T", " T")

        # Display the information in a Pandas DataFrame for better formatting
        st.subheader("Transport Options")
        df = pd.DataFrame(list(filtered_info.items()), columns=['Option', 'Details'])

        # Apply consistent styling to both the headers and the body of the table
        styled_df = df.style.set_properties(**{
            'background-color': 'black',
            'color': 'white',
            'border-color': 'gray',
            'border-style': 'solid',
            'border-width': '1px'
        }).set_table_styles([{
            'selector': 'thead th',
            'props': [('background-color', 'black'), ('color', 'white')]
        }, {
            'selector': 'tbody td',
            'props': [('background-color', 'black'), ('color', 'white')]
        }, {
            'selector': 'tr:hover',
            'props': [('background-color', '#333333')]
        }]).hide_index()

        # Displaying styled DataFrame without indices
        st.write(styled_df.to_html(), unsafe_allow_html=True)

        train_station_address = get_train_station_address(connection_info)
        if train_station_address:
            train_station_coords = google_maps.get_coordinates_from_address(train_station_address)
            if train_station_coords:
                st.subheader("Train Station Location")

                # Create a DataFrame for pydeck
                train_station_df = pd.DataFrame([train_station_coords], columns=['latitude', 'longitude'])

                # Define a pydeck Layer for the train station location
                train_station_layer = pdk.Layer(
                    "ScatterplotLayer",
                    train_station_df,
                    get_position='[longitude, latitude]',
                    get_color='[0, 0, 255, 160]',  # Blue color for train station
                    get_radius=50,
                )

                # Set the viewport location
                train_station_view_state = pdk.ViewState(
                    latitude=train_station_coords['latitude'],
                    longitude=train_station_coords['longitude'],
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
