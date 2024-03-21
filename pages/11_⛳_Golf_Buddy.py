import streamlit as st
import base64
import src.golf_buddy_11 as app
import json
st.set_page_config(layout='wide')
# Create three columns
st.title("⛳ Golf Buddy")

def create_video_html(file):
    with open(file, "rb") as file:
        video_encoded = base64.b64encode(file.read()).decode()
    video_tag = f'<video width="320" height="240" controls><source src="data:video/mp4;base64,{video_encoded}" type="video/mp4"></video>'
    return video_tag

def create_gif_html(file_path):
    return f'<img src="{file_path}" width="200"/>'
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the capabilities of the Multimodal Gemini to analyze golf swings. It was fed with TopTracer screenshots via DocumentAI to read statistics. It also uses Vertex Search to provide context information about golf rules"
    how_to_use = "Upload a video of your golf swing, select the club used, and the distance achieved. The model will analyze the swing and provide tips to improve the swing."
    services_used = "Vertex AI, Gemini Pro Vision, Vertex Search, Document AI"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()
    
col1, col2, col3 = st.columns(3)



# First column: file uploaders for the videos
with col1:
    st.header("Upload your videos")
    front_swing = st.file_uploader("Front golf swing video", type=["mp4", "mov", "avi", "wmv", "flv", "mkv", "webm", "m4v", "mpg", "mpeg", "3gp", "3g2", "mxf", "roq", "nsv", "flv", "f4v", "f4p", "f4a", "f4b"])
    with open("assets/11_golf_buddy.MP4", "rb") as file:
        btn = st.download_button(
            label="Download sample video",
            data=file,
            file_name="11_golf_buddy.MP4",
            mime="video/mp4"
            )
    
    if front_swing:
        front_swing = open("assets/11_golf_buddy.MP4", "rb")
        with open('temp/front_swing.mp4', 'wb') as f:
            f.write(front_swing.read())
        
        
with col2:
    st.header("Club and distance")
    club = st.selectbox("Select your club", ["Driver", "3-wood", "7-iron", "Pitching Wedge"])
    distance = st.slider("Enter the distance achieved", min_value=0, max_value=400, value=200, step=10)
    st.write(f"You selected {club} and {distance} meters")
    if st.button("Give me tips"):
        with st.spinner("Analyzing your swing..."):
            swing = app.button_started(front_swing, club, distance)
            st.subheader("Tips")
            for tip in swing["tips"]:
                st.write(f"*{tip['emoji']} {tip['tip']}*", key=tip['tip'])
            st.subheader("Positive feedback")
            for positive in swing["positives"]:
                st.write(f"*✅{positive['feedback']}*")
            with col3:
                st.header("Your swing")
                for tip in swing["tips"]:
                    st.write(f"**{tip['tip']}**")
                    st.write("**Explanation:** ", tip["explanation"])
                    st.write("**Why:**", tip["why"])
        



