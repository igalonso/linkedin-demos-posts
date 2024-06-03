import streamlit as st
import src.reasoning_engine_job_finder as app
import uuid

st.session_state['show_text'] = False
st.set_page_config(
    layout="wide",
    page_title="",
    initial_sidebar_state="expanded",
)
st.title('🔍 Reasoning Engine Job Finder')
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


# chat_hi
# story = []


# prompt = "Give me a list of the job offers in New York as a Data Engineer with the salary in EUR. Rate them from best to worse. Include a brief description of the benefits."
# response= app.agent_invoke(prompt,random_uuid)

# print("INPUT: " + response["input"])
# print("OUTPUT: "+ response["output"])
# print("-------------------------------INTERMIDIATE STEPS-------------------------------")
# print(response["intermediate_steps"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_uuid():
    if 'uuid' not in st.session_state:
        # If not, generate a new UUID and store it in the session state
        st.session_state.uuid = str(uuid.uuid4())

    # Return the UUID from the session state
    return st.session_state.uuid

random_uuid = generate_uuid()  

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
system_prompt = "You are an agent that helps people find jobs. You can provide information about job offers, salaries, and benefits. You can also provide advice on how to find a job. You are friendly and use emojis a lot."
system_prompt =""
# React to user input
if prompt := st.chat_input("Do you want to find a job?"):
    # Display user message in chat message container
    final_prompt = system_prompt + "\n" + prompt
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = app.agent_invoke(final_prompt,random_uuid)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response["output"])
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response["output"]})