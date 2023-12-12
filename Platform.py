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
import requests
from utils import google_maps
from utils import public_transport
from utils import tier

print(tier.get_vehicles_in_range(48.1, 16.3, 1500))
# Streamlit App Layout
st.set_page_config(page_title="Transportation Helper", layout="wide")
st.title("Transportation Helper")

# Input for manual address entry
with st.form("address_input"):
    start_address = st.text_input("Enter your starting address:")
    end_address = st.text_input("Enter your destination address:")
    submitted_address = st.form_submit_button("Find Transport Options with Address")

# Map for location selection
st.subheader("Or click on the map to set your starting location:")
map_location = st.map()
submitted_map = False
if map_location:
    submitted_map = st.button("Find Transport Options with Map")

# Processing the input
if submitted_address and start_address and end_address:
    now = datetime.now()
    depart_date = now.strftime("%Y-%m-%d")
    depart_time = now.strftime("%H:%M")
    connection_info = public_transport.find_connection(start_address, end_address, depart_date, depart_time)
    st.write(connection_info)

elif submitted_map and map_location:
    # Assuming the first clicked location is the starting point
    start_lat, start_lon = map_location["lat"], map_location["lon"]
    start_address = google_maps.get_nearest_station(start_lat, start_lon)
    st.write(f"Nearest Station: {start_address}")

    end_address = st.text_input("Enter your destination address:")
    if end_address:
        now = datetime.now()
        depart_date = now.strftime("%Y-%m-%d")
        depart_time = now.strftime("%H:%M")
        connection_info = public_transport.find_connection(start_address, end_address, depart_date, depart_time)
        st.write(connection_info)

# Additional feature: Find nearby scooters
st.subheader("Find Nearby Scooters")
latitude = st.number_input("Latitude", value=48.1)
longitude = st.number_input("Longitude", value=16.3)
radius = st.number_input("Radius (in meters)", value=1500)
if st.button("Find Scooters"):
    scooter_info = tier.get_vehicles_in_range(latitude, longitude, radius)
    st.write(scooter_info)

# you can multiply the walking speed from google maps by the corresponding mode of transport's speed
