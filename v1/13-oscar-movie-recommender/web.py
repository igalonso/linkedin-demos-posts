import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import app

st.set_page_config(
    # page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="Movie Recommender",
    initial_sidebar_state="expanded",
)

# Create a Streamlit layout with two columns
col1, col2 = st.columns(2)

# Generate word clouds in the first column
with col1:
    st.header("Movie Categories and Oscar Winners")
    # Create a multiselect widget for categories
    selected_categories = st.multiselect('Select Categories', app.return_unique_categories())
    # Create a multiselect widget for movies
    selected_movies = st.multiselect('Select movies', app.return_unique_movies())
    
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
            
