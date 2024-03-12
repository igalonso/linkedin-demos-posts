import streamlit as st
from src.contact_center_enhancer_10 import transcribe_audio_file, calling_gemini_magic

st.title("Contact Center GenAI Enhancer")

st.subheader("Upload an audio file of a customer service call and get a summary of the conversation, the sentiment, and the category of the call.")

def get_background_color_sentiment(sentiment):
    if sentiment == "positive":
        return "#00cc00"
    elif sentiment == "negative":
        return "#ff0000"
    elif sentiment == "neutral":
        return "#ffcc00"
    else:
        return "#000000"

def get_background_color_category(category):
    if category == "sales":
        return "#ffcc00"
    elif category == "support":
        return "#00cc00"
    elif category == "billing":
        return "#ff0000"
    else:
        return "#000000"
def get_background_color_next_action(next_action):
    if next_action == "follow_up":
        return "#ffcc00"
    elif next_action == "no_follow_up":
        return "#00cc00"
    elif next_action == "escalate":
        return "#ff0000"
    elif next_action == "no_escalate":
        return "#000000"
    elif next_action == "upsell":
        return "#ffcc00"
    elif next_action == "cross_sell":
        return "#00cc00"
    elif next_action == "no_upsell":
        return "#ff0000"
    elif next_action == "no_cross_sell":
        return "#000000"
    else:
        return "#000000"


col1, col2, col3 = st.columns(3)
with col1:
    audio_file = st.file_uploader("Upload an audio file", type=["wav"])
    if audio_file is not None:
        st.audio(audio_file)
    generate = st.button("Transcribe")

if generate:
    with st.spinner('Transcribing audio file...'):
        with col2: 
            summary = transcribe_audio_file(audio_file, "telephony")
            # response = transcribe_audio_file("commercial_stereo.wav", "telephony")
            for alternative in summary:
                if alternative.channel_tag == 1:
                    if alternative.alternatives[0].transcript != "":
                        st.write(":robot_face:: " +alternative.alternatives[0].transcript)
                else:
                    if alternative.alternatives[0].transcript != "":
                        st.write(":ghost:: " +alternative.alternatives[0].transcript)
        with col3:
            conclussions = calling_gemini_magic(summary)
            st.write("**Summary of conversation:** "+ conclussions['summary_of_conversation'])
            st.markdown(f'**Sentiment:** <div style="display: inline-block; padding: 0.25em 0.5em; border-radius: 15px; background-color: {get_background_color_sentiment(conclussions["sentiment"])}; color: white;">{conclussions["sentiment"]}</div>', unsafe_allow_html=True)
            st.write("**Sentiment reason:** "+ conclussions['sentiment_reason'])
            st.markdown(f'**Category:** <div style="display: inline-block; padding: 0.25em 0.5em; border-radius: 15px; background-color: {get_background_color_category(conclussions["category"])}; color: white;">{conclussions["category"]}</div>', unsafe_allow_html=True)
            st.markdown(f'**Next action:** <div style="display: inline-block; padding: 0.25em 0.5em; border-radius: 15px; background-color: {get_background_color_next_action(conclussions["next_action"])}; color: white;">{conclussions["next_action"]}</div>', unsafe_allow_html=True)