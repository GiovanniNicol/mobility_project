
import streamlit as st
import pandas as pd
import numpy as np

st.header('FindMyWay :world_map:', divider='blue')
st.markdown("*Group project 3.4*")

st.subheader('Hey you :blush:')
st.subheader('Just enter now your location address and the nearest mobility connections will be shown on the map below :arrow_down:')

destination_address = st.text_input("My destination is:")

zurich_coordinates = [47.3769, 8.5417]
   
df = pd.DataFrame(
   np.random.randn(700, 2) / [70, 70] +  zurich_coordinates,
    columns=['lat', 'lon']
)

st.map(df)

# you can multiply the walking speed from google maps by the corresponding mode of transport's speed


    
   

