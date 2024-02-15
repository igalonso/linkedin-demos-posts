import streamlit as st
import app

st.set_page_config(
    # page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="Tell me a story!",
    initial_sidebar_state="expanded",
)


# Create 3 columns
col1, col2, col3 = st.columns(3)

# In the first column, ask for the name and age of the kid
with col1:
    st.header("Kid's Information")
    kid_name = st.text_input("Kid's Name")
    kid_age = st.number_input("Kid's Age", min_value=1)

# In the third column, create placeholders for generated text and audio
with col3:
    st.header("Generated Content")
    

# In the second column, ask for the things the kid likes
with col2:
    st.header("Kid's Interests")
    kid_interests = st.text_input("Things the Kid Likes")
    if st.button("Generate Story"):
        with col3:
            story = app.generate_story(kid_name, kid_age, kid_interests)
            print(story)
            app.narrate_story(story, "story.mp3")
            audio_file = open("story.mp3", "rb")
            st.audio(audio_file, format="audio/mp3")
            story_paragraphs = story.split("\n\n")
            story_images = []
            i = 0
            for paragraph in story_paragraphs:
                st.write(paragraph)
                if "boy" not in paragraph and i % 2 == 0:
                    summary = app.generate_summary(paragraph)
                    try:
                        images = app.generate_kid_images(paragraph,summary)
                    except:
                        print("ouch on image")
                    try:
                        for img in images:
                            story_images.append(img)
                            st.image(img, width=300)
                            
                    except:
                        print("ouch")
                i = i+1