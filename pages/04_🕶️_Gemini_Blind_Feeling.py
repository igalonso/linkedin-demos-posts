import streamlit as st
import time
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

from src.blind_feeling_demo_04 import *
st.session_state['show_text'] = False

st.set_page_config(
    # page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="🕶️ Blind Feeling Demo",
    initial_sidebar_state="expanded",
)
st.title("🕶️ Blind Feeling Demo")
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the multimodal capabilities of Gemini. The user can upload a photo and the model will generate a description of the photo for blind people. The model also will selecta suitable song for the picture and play it "
    how_to_use = "Upload a photo and the model will generate a description of the photo for blind people. The model also will selecta suitable song for the picture and play it"
    services_used = "Vertex AI, Gemini pro vision, Spotify API"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Choose a photo")
    with open("assets/image.jpg", "rb") as file:
        btn = st.download_button(
            label="Download sample image",
            data=file,
            file_name="image.jpg",
            mime="image/jpg"
        )
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    redirect_url = os.environ.get('SPOTIPY_REDIRECT_URI')
    st.text_input("Enter your Spotify Client ID", key="client_id", value=client_id)
    st.text_input("Enter your Spotify Client Secret", key="client_secret", value=client_secret)
    st.text_input("Enter your Spotify Redirect URL", key="redirect_url", value=redirect_url)
    if uploaded_file:
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
        with col2: 
            st.write(f"**Description**: {description['description']}")
            st.write(f"**Song Name**: {description['song_name']}")
            st.write(f"**Author**: {description['author']}")
            st.write(f"**Reasoning**: {description['reasoning']}")
            if client_id and client_secret and redirect_url:
                start_song(description['song_name'], description['author'],client_id, client_secret,redirect_url)
            audio = text_to_speech(description['description'], 'description.mp3')
            st.audio(audio, format='audio/mp3')
