import streamlit as st
from app import transcribe_audio_file, calling_gemini_magic

st.title("Contact Center GenAI Enhancer")

st.subheader("Upload an audio file of a customer service call and get a summary of the conversation, the sentiment, and the category of the call.")

col1, col2, col3 = st.columns(3)
with col1:
    audio_file = st.file_uploader("Upload an audio file", type=["wav"])
    if audio_file is not None:
        st.audio(audio_file)
    generate = st.button("Transcribe")

if generate:
    with st.spinner('Reading and summarizing document...'):
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
            st.write("**Sentiment:** "+ conclussions['sentiment'])
            st.write("**Sentiment reason:** "+ conclussions['sentiment_reason'])
            st.write("**Category:** "+ conclussions['category'])
            st.write("**Next action:** "+ conclussions['next_action'])
            # st.subheader("Summary of conversation")
            # st.write(conclussions['summary_of_conversation'])
            # st.subheader("Sentiment")
            # st.write(conclussions['sentiment'])
            # st.subheader("Sentiment reason")
            # st.write(conclussions['sentiment_reason'])
            # st.subheader("Category")
            # st.write(conclussions['category'])
            # st.subheader("Next action")
            # st.write(conclussions['next_action'])
            