import streamlit as st
from streamlit.components.v1 import html


st.set_page_config(
    layout="wide",
    page_title="🦾 #oneweekoneusecase Agent",
    initial_sidebar_state="expanded",
)
st.title('🦾 #oneweekoneusecase Agent')
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False
if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases how easy is building an Agent using Agent Builder and use it as an assistant of you web"
    how_to_use = "Start a chat and talk about the demos."
    services_used = "Vertex AI, Agent Builder"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()

# Create the main layout of the web page
main_col1, main_col2= st.columns(2)

link = """
<link rel="stylesheet" href="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/themes/df-messenger-default.css">
"""
script = """
<script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>
    <df-messenger
    location="us-central1"
    project-id="gen-ai-igngar"
    agent-id="f0a2cf07-9b7d-4b71-a24e-f3b15ee2c6f8"
    language-code="en"
    max-query-length="-1">
    <df-messenger-chat-bubble
    chat-title="">
    </df-messenger-chat-bubble>
    </df-messenger>
"""
style = """
<style>
  df-messenger {
    z-index: 999;
    position: absolute;
    --df-messenger-font-color: #000;
    --df-messenger-font-family: Google Sans;
    --df-messenger-chat-background: #f3f6fc;
    --df-messenger-message-user-background: #d3e3fd;
    --df-messenger-message-bot-background: #fff;
    bottom: 16px;
    right: 16px;
  }
</style>
"""
all_html = link+script + style
with main_col1:
    st.write("Chat with the Agent by clicking the bottom right corner chat icon.")
with main_col2:
    html(all_html,height=800)