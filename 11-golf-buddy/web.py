import streamlit as st
import base64
import app
import json
from st_files_connection import FilesConnection
st.set_page_config(layout='wide')
# Create three columns
st.title("⛳ Golf Buddy ⛳")

def create_video_html(file):
    with open(file, "rb") as file:
        video_encoded = base64.b64encode(file.read()).decode()
    video_tag = f'<video width="320" height="240" controls><source src="data:video/mp4;base64,{video_encoded}" type="video/mp4"></video>'
    return video_tag

def create_gif_html(file_path):
    return f'<img src="{file_path}" width="200"/>'

col1, col2, col3 = st.columns(3)

# First column: file uploaders for the videos
with col1:
    st.header("Upload your videos")
    front_swing = st.file_uploader("Front golf swing video", type=["mp4", "mov", "avi", "wmv", "flv", "mkv", "webm", "m4v", "mpg", "mpeg", "3gp", "3g2", "mxf", "roq", "nsv", "flv", "f4v", "f4p", "f4a", "f4b"])
    if front_swing is not None:
        with open('front_swing.mp4', 'wb') as f:
            f.write(front_swing.read())
        st.markdown(create_video_html("front_swing.mp4"), unsafe_allow_html=True)
    # posture = st.file_uploader("Image of your swing posture", type=["jpeg", "png", "jpg", "webp"])
    # if posture is not None:
    #     st.image(posture)
    # hand_grip = st.file_uploader("Hand grip video", type=["jpeg", "png", "jpg", "webp"])
    # if hand_grip is not None:
    #     st.image(hand_grip)

# Second column: selectbox for the club and number input for the distance
with col2:
    st.header("Club and distance")
    club = st.selectbox("Select your club", ["Driver", "3-wood", "7-iron", "Pitching Wedge"])
    distance = st.slider("Enter the distance achieved", min_value=0, max_value=400)
    st.write(f"You selected {club} and {distance} meters")
    if st.button("Give me tips"):
        with st.spinner("Analyzing your swing..."):
            swing, positive = app.button_started(front_swing, club, distance)
            st.subheader("Tips")
            for tip in swing["tips"]:
                st.write(f"*{tip['emoji']} {tip['tip']}*", key=tip['tip'])
            st.subheader("Positive feedback")
            for positive in positive:
                st.write(f"*✅{positive['feedback']}*")
            with col3:
                st.header("Your swing")
                for tip in swing["tips"]:
                    st.write(f"**{tip['tip']}**")
                    st.write("**Explanation:** ", tip["explanation"])
                    st.write("**Why:**", tip["why"])
            # else:
            #     st.error("Please upload all the videos and images")
        
        



