import streamlit as st
import pandas as pd
import numpy as np

st.header('FindMyWay :world_map:', divider='blue')

st.subheader('Hey you :blush:')
st.subheader('Just enter now your location address and the nearest mobility connections will be shown on the map below :arrow_down:')

destination_address = st.text_input("My destination is:")

zurich_coordinates = [47.3769, 8.5417]
   
df = pd.DataFrame(
   np.random.randn(700, 2) / [70, 70] +  zurich_coordinates,
    columns=['lat', 'lon']
)

st.map(df)

#NOTES#
# Koordinaten für Zürich
# zurich_coordinates = [47.3769, 8.5417]

# DataFrame erstellen
# df = pd.DataFrame(
# #     np.random.randn(1000, 2) / [50, 50] + zurich_coordinates,
#     columns=['lat', 'lon']
# 
# # Koordinaten für Zürich
# zurich_coordinates = [47.3769, 8.5417]

# DataFrame erstellen
# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + zurich_coordinates,
  #   columns=['lat', 'lon'])

# Ausgabe des DataFrames
# print(df)
# 






#def display_result(destination):
   # st.success("Submission successful!")
   # st.write(f"Destination: {destination}")
    
   
   # geolocator = Nominatim(user_agent="geocoder")
   # location = geolocator.geocode(destination)

   # if location:
      
   #     st.map(location.raw["latlon"])
        
     
    #    st.sidebar.header("Additional Information")
        

    #    if st.sidebar.button("Train Information"):
    #        # Replace with actual train information retrieval logic or link
     #       st.sidebar.write("Train information will be displayed here.")
        
    
     #   if st.sidebar.button("Mobility App"):
      #      # Replace with the actual link or logic to open the mobility app
     #       st.sidebar.write("Link to the mobility app will be opened.")
        
     
    #    st.info("Enjoy your journey! We're looking forward to seeing you again.")
    #else:
#        st.warning("Unable to find coordinates for the entered destination.")

#if __name__ == "__main__":
#    main()

    
   

