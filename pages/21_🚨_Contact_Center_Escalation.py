import streamlit as st
from src.contact_center_escalation_21 import transcribe_audio_file, get_call_meta_info, agent_invoke
import uuid
st.session_state['show_text'] = False
st.set_page_config(
    # page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="🚨 Contact Center Escalation",
    initial_sidebar_state="expanded",
)
st.title("🚨 Contact Center Escalation")

if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the capabilities of GenAI to enhance contact center services. The user can upload an audio file of a customer service call and the model will provide a summary of the conversation, the sentiment, and the category of the call."
    how_to_use = "Upload an audio file of a customer service call and get a summary of the conversation, the sentiment, and the category of the call."
    services_used = "Vertex AI, Gemini Pro, Speech-to-Text API, Model Garden"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()
def generate_uuid():
    if 'uuid' not in st.session_state:
        # If not, generate a new UUID and store it in the session state
        st.session_state.uuid = str(uuid.uuid4())

    # Return the UUID from the session state
    return st.session_state.uuid

random_uuid = generate_uuid()  
# st.subheader("Upload an audio file of a customer service call and get a summary of the conversation, the sentiment, and the category of the call.")

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

def execute_agent_3_times(iteration:int, conclussions:dict, email:str):
    if iteration == 0:
        return "No response"
    else:
        try:
            response = agent_invoke(conclussions, email)
            print(response)
            return response
        except Exception as e:
            response = execute_agent_3_times(iteration-1,conclussions, email)
            print(response)
            return response
        
def execute_agent_call_meta_info_3_times(iteration:int, audio_data:bytes):
    if iteration == 0:
        return "No response"
    else:
        try:
            conclussions = get_call_meta_info(audio_data)
            print(conclussions)
            return conclussions
        except Exception as e:
            conclussions = execute_agent_call_meta_info_3_times(iteration-1,audio_data)
            print(conclussions)
            return conclussions
        




col1, col2, col3 = st.columns(3)
with col1:
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg", "flac"])
    with open("assets/angry_customer.mp3", "rb") as file:
        btn = st.download_button(
            label="Download sample audio",
            data=file,
            file_name="angry_customer.mp3",
            mime="audio/mp3"
        )
    if audio_file:
        st.audio(audio_file)
if audio_file:
    with st.spinner('Transcribing audio file...'):
        
        audio_data = audio_file.read()
        with col2:
            
            
            transcription = transcribe_audio_file(audio_data)
            for speaker in transcription['transcription']:
                if speaker['speaker'] == "1":
                    st.write(":robot_face:: " +speaker['text'])
                else:
                    st.write(":ghost:: " +speaker['text'])
    
        with col3:
            conclussions = execute_agent_call_meta_info_3_times(3,audio_data)
            if conclussions == "No response":
                st.write("No response")
            else:
                # get_call_meta_info(audio_data)
                print(conclussions)
                st.write("**Summary of conversation:** "+ conclussions['summary_of_conversation'])
                st.markdown(f'**Sentiment:** <div style="display: inline-block; padding: 0.25em 0.5em; border-radius: 15px; background-color: {get_background_color_sentiment(conclussions["sentiment"])}; color: white;">{conclussions["sentiment"]}</div>', unsafe_allow_html=True)
                st.write("**Sentiment reason:** "+ conclussions['sentiment_reason'])
                st.markdown(f'**Category:** <div style="display: inline-block; padding: 0.25em 0.5em; border-radius: 15px; background-color: {get_background_color_category(conclussions["category"])}; color: white;">{conclussions["category"]}</div>', unsafe_allow_html=True)
                st.markdown(f'**Next action:** <div style="display: inline-block; padding: 0.25em 0.5em; border-radius: 15px; background-color: {get_background_color_next_action(conclussions["next_action"])}; color: white;">{conclussions["next_action"]}</div>', unsafe_allow_html=True)
                response = execute_agent_3_times(3,conclussions, "security@contanctcenterenhancer.com")
                if response != "No response":
                    st.subheader("Agent Automated response")
                    st.write("**Action:** "+ response['output'])
                    st.write("**Email sent:** "+ response['intermediate_steps'][0][1])
                else:
                    st.write("**Action:** No response.")