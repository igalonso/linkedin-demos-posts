import streamlit as st
import time
import numpy as np
import os

from src.blind_feeling_demo_04 import *



st.set_page_config(page_title="Blind Feeling Demo", page_icon="🕶️")

st.markdown("# Blind Feeling Demo")
st.sidebar.header("Blind Feeling Demo")

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Choose a photo")
    if uploaded_file is not None:
        image = st.image(uploaded_file)
        # Create the temp directory if it doesn't exist
        if not os.path.exists('temp'):
            os.makedirs('temp')
        # Write the uploaded file to disk
        with open(os.path.join('temp', uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getvalue())
        img = os.path.join('temp', uploaded_file.name)
        metadata = get_geotagging(img)

        # Get the latitude and longitude in decimal degrees
        lat = get_decimal_from_dms(metadata['GPSLatitude'], metadata['GPSLatitudeRef'])
        lon = get_decimal_from_dms(metadata['GPSLongitude'], metadata['GPSLongitudeRef'])
        address = get_location_by_coordinates(lat, lon)
        description = agent_start(0, address,img )
        description = description.replace('```json', '')
        description = description.replace('```', '')
        description = json.loads(description)
        st.write(f"**Description**: {description['description']}")
        st.write(f"**Song Name**: {description['song_name']}")
        st.write(f"**Author**: {description['author']}")
        st.write(f"**Reasoning**: {description['reasoning']}")
        start_song(description['song_name'], description['author']) #fix this
        text_to_speech(description['description'], 'description.mp3')
