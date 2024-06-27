import streamlit as st
import src.it_support_helper_22 as app
import uuid

st.session_state['show_text'] = False
st.set_page_config(
    layout="wide",
    page_title="",
    initial_sidebar_state="expanded",
)
st.title('💻 IT Service Agent')
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False
if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases how easy is to integrate Vertex AI in Langchain."
    how_to_use = "Start a chat and ask for a job and the result in Euros."
    services_used = "Vertex AI in Langchain"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_uuid():
    if 'uuid_IT_Service' not in st.session_state:
        # If not, generate a new UUID and store it in the session state
        st.session_state.uuid_IT_Service = str(uuid.uuid4())

    # Return the UUID from the session state
    return st.session_state.uuid_IT_Service

random_uuid = generate_uuid()  

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
system_prompt = ""
system_prompt ="You are an IT Service agent that helps users with their IT problems. These IT problems can be complex or simple user stuff. You need to help solve the issue using the tools you have to gather information of past occurrences of the issue."
# React to user input
if prompt := st.chat_input("What is your IT problem?"):
    # Display user message in chat message container
    final_prompt = system_prompt + "\n" + prompt
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    print(random_uuid)
    response = app.agent_invoke(prompt, random_uuid)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response["output"])
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response["output"]})