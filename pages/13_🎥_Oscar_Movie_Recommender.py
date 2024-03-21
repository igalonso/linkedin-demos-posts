import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import src.oscars_movie_recommender_13 as app

st.set_page_config(
    # page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="🎥 Oscar Movie Recommender",
    initial_sidebar_state="expanded",
)
st.title("🎥 Oscar Movie Recommender")
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the capabilities of Gemini to recommend movies based on categories and Oscar winners. We used BigQuery to gather the data and Gemini to create the recommendation model. The user can select categories and movies and the model will recommend a movie based on the categories and movies selected."
    how_to_use = "Select categories and movies and click on the button to get a movie recommendation. The model will recommend a movie based on the categories and movies selected."
    services_used = "Vertex AI, Gemini, BigQuery ML"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()

# Create a Streamlit layout with two columns
col1, col2 = st.columns(2)

# Generate word clouds in the first column
with col1:
    # st.header("Movie Categories and Oscar Winners")
    # Create a multiselect widget for categories
    selected_categories = st.multiselect('Select Categories', app.return_unique_categories(), default=["drama", "fantasy"])
    # Create a multiselect widget for movies
    selected_movies = st.multiselect('Select movies', app.return_unique_movies(),default=["2022, Avatar: The Way of Water", "2022, Top Gun: Maverick"])
    
    # Button for movie recommendations
    if st.button('Recommend me movies'):
        # Call your recommendation system here and store the result in recommended_movies
        with col2:            
            recommended_movies = app.recommend_movies(selected_categories,selected_movies)
            st.header("Recommended Movie")
            st.image(recommended_movies["poster"])
            st.subheader(recommended_movies["movie_recommendation"])
            st.subheader("Why?")
            st.write(recommended_movies["recommendation_reason"])
            st.subheader("Plot")
            st.write(recommended_movies["plot"])
            
