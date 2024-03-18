import streamlit as st
import base64

import sys
sys.path.insert(1, '')

import src.react_agents_demo_agent_02 as agent
import os

st.set_page_config(
    page_icon="assets/robot-1.1s-200px.png",
    layout="wide",
    page_title="React Agents Demo with Vertex AI (Google Cloud)",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"<div class='header'><h3> React Agents Demo</h3></div>",
    unsafe_allow_html=True,
)
# st.markdown(
#     f'<div>Welcome to the ReAct! We are going to do an example of a nice job offer to a candidate. For that we need to do some steps:<ul><li>Our recruiter agent will gather information about the candidate and the company using Tools.</li><li>That information will be shared with the HR department who is resposible to allocate budget for the salary.</li><li>With this information, the recruiter is going to draft an email to the candidate to explaion the position and the salary offer.</li></ul>LETS GO!</div>',
#     unsafe_allow_html=True
# )
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    st.markdown('<span style="word-wrap:break-word;">Showcase what GenAI can do further than chatbots and search. Use agents to automate processes. In this case, we are going to do an example of a nice job offer to a candidate. For that we need to do some steps:\n- Our recruiter agent will gather information about the candidate and the company using Vertex AI.\n- That information will be shared with the HR department who is resposible to allocate budget for the salary.\n- With this information, the recruiter is going to draft an email to the candidate to explaion the position and the salary offer.\n</span>', unsafe_allow_html=True)
    st.image("assets/diagram.png", width=700)
    st.markdown("**How to use the demo:**")
    st.markdown('<span style="word-wrap:break-word;">Fill the form with the information of the candidate and the company. Select the models for the agents and the temperature for the text generation. Click on the button to run the agents and wait for the results. The recruiter will gather information about the candidate and the company, then the HR department will allocate budget for the salary and finally the recruiter will draft an email to the candidate to explain the position and the salary offer.</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown("Vertex AI, Model Garden, PaLM, Gemini, Gmail API, Vertex Search, langchain")
    st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    full_name = st.text_input("Full Name of Candidate", value="Ignacio Garcia")
    company_name = st.text_input("Full Name of the company offering", value="Nintendo")
    position=st.text_input("Full Name of the postion offered",value="Solutions Architect")
    testing = st.checkbox("Testing", value=True)
    email_to_send_to = st.text_input("Email to send the draft", value="example@gmail.com")
with col2:
    
    model_for_information_gathering = st.selectbox("Select a model for information gathering", ("text-bison@002","text-bison@001", "text-unicorn","gemini-pro"))
    model_for_hr_salary_decision = st.selectbox("Select a model for HR salary decision", ("text-bison@001","text-bison@002", "text-unicorn","gemini-pro"))
    model_for_email_draft = st.selectbox("Select a model for email draft", ("text-unicorn", "text-bison@001","text-bison@002","text-bison-32k"))
    temperature_slider = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    temperature_slider_email = st.slider("Temperature for email", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    verbose = False
    generate = st.button("Run Agent🤖")
    os.environ["TEMPERATURE_AGENTS"] = str(temperature_slider)
    os.environ["TEMPERATURE_EMAIL"] = str(temperature_slider_email)

file_ = open(os.getcwd()+"/assets/info_agent.gif", "rb")
contents = file_.read()
info_agent_image = base64.b64encode(contents).decode("utf-8")
file_.close()
file_ = open(os.getcwd()+"/assets/hr_agent.gif", "rb")
contents = file_.read()
hr_agent_image = base64.b64encode(contents).decode("utf-8")
file_.close()
file_ = open(os.getcwd()+"/assets/email_agent.gif", "rb")
contents = file_.read()
email_agent_image = base64.b64encode(contents).decode("utf-8")
file_.close()

if generate:

    with st.spinner("Agent running..."):
        os.environ["VERTEX_MODEL_GATHERING"] = model_for_information_gathering
        os.environ["VERTEX_MODEL_SALARY"] = model_for_hr_salary_decision
        os.environ["VERTEX_MODEL_EMAIL"] = model_for_email_draft
        os.environ["TESTING"] = str(testing)
        
        with col3:
            info_agent_md = st.markdown(
                f'<div class="gif_holder"><img  src="data:image/gif;base64,{info_agent_image}" alt="Info Agent GIF" style="border: solid red; width: 100%"></div>',
                unsafe_allow_html=True,
            )

        candidate_summary = agent.recruiter_personal_inspection(position, company_name, full_name, verbose)["output"]
        with col3:
            info_agent_md.empty()
            hr_agent_md = st.markdown(
            f'<div class="gif_holder"><img  src="data:image/gif;base64,{hr_agent_image}" alt="HR Agent GIF" style="border: solid red; width: 100%"></div>',
                unsafe_allow_html=True,
            )
        salary_offer = agent.hr_salary_estimation(candidate_summary, verbose)["output"]
        print(salary_offer)
        candidate_summary = candidate_summary + "\n- Salary Offer: " + salary_offer+ "\n"
        # output.empty()
        with col3:
            hr_agent_md.empty()
            email_agent_md = st.markdown(
                f'<div class="gif_holder"><img  src="data:image/gif;base64,{email_agent_image}" alt="HR Agent GIF" style="border: solid red; width: 100%"></div>',
                unsafe_allow_html=True,
            )
        agent.recruiter_email_creator(candidate_summary,full_name, company_name, position,email_to_send_to, verbose)
        email_agent_md.empty()
        st.balloons()
        st.success("Agent finished! - Now you can access your mail to find out the draft offer. Keep in mind that it could be in your spam folder.")  
        # st.write("[gmail link to drafts](https://mail.google.com/mail/u/0/#drafts)")