import streamlit as st
import src.conference_connect_17 as  app
st.session_state['show_text'] = False
st.set_page_config(
    layout="wide",
    page_title="🤝 Conference Connect",
    initial_sidebar_state="expanded",
)
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False
if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcase a simple genai application that matches conference attendees based on their interests."
    how_to_use = "Select one of the 3 attendees and a list of attendees with similar interests will be displayed."
    services_used = "Vertex AI, Gemini"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()

attendees_to_be_selected = [
    {
        "Name": "Jack",
        "Surname": "Doe",
        "Email": "john.doe@techcorp.io",
        "Company Name": "TechCorp",
        "Category of the company": "Software Development",
        "Interests": ["App Engine", "Compute Engine", "Go", "Kubernetes"],
        "Job Title": "Software Engineer",
        "Customer": "no",
        "Prospect": "yes",
        "Recent Projects using Google Cloud": "Developed a scalable web application using App Engine"
    },
    {
        "Name": "Jane",
        "Surname": "Smith",
        "Email": "jane.smith@analyticspro.com",
        "Company Name": "Analytics Pro",
        "Category of the company": "Data Analytics",
        "Interests": ["BigQuery", "Dataflow", "Machine Learning", "R"],
        "Job Title": "Data Scientist",
        "Customer": "yes",
        "Prospect": "no",
        "Recent Projects using Google Cloud": "Predictive analytics model using BigQuery ML"
    },
    {
        "Name": "Alice",
        "Surname": "Johnson",
        "Email": "alice.johnson@cloudsolutions.com",
        "Company Name": "Cloud Solutions",
        "Category of the company": "Cloud Services",
        "Interests": ["Cloud Storage", "Cloud Functions", "Python", "Firebase"],
        "Job Title": "Cloud Architect",
        "Customer": "yes",
        "Prospect": "yes",
        "Recent Projects using Google Cloud": "Serverless architecture using Cloud Functions"
    }
]

# Create the main layout of the web page
main_col1, main_col2= st.columns(2)
with main_col1:
    st.header("Attendees")
    attendees = ['Jack', 'Jane', 'Alice']
    selected_attendee = st.selectbox("Select an attendee", attendees)
    if selected_attendee == 'Jack':
        id = 0
    elif selected_attendee == 'Jane':
        id = 1
    else:
        id = 2
    st.write("**Name:** " + attendees_to_be_selected[id]['Name'])
    st.write("**Surname:** " + attendees_to_be_selected[id]['Surname'])
    st.write("**Email:** " + attendees_to_be_selected[id]['Email'])
    st.write("**Company:** " + attendees_to_be_selected[id]['Company Name'])
    st.write("**Category of the company:** " + attendees_to_be_selected[id]['Category of the company'])
    
    interests = ""
    for interest in attendees_to_be_selected[id]['Interests']:
        interests = interests + interest + ", "
    st.write("**Interests:** " + interests)
    st.write("**Job Title:** " + attendees_to_be_selected[id]['Job Title'])

if selected_attendee:
    with main_col2:
        st.header("Connect with these fellow attendees!")
        if selected_attendee == 'Jack':
            id = 0
        elif selected_attendee == 'Jane':
            id = 1
        else:
            id = 2
        texts = ""
        for interest in attendees_to_be_selected[id]['Interests']:
            texts =texts + interest
        texts = texts + attendees_to_be_selected[id]['Recent Projects using Google Cloud']
        texts = texts + attendees_to_be_selected[id]['Job Title']
        similar_attendees = app.get_vector_search(texts)
        # st.write(similar_attendees)
        for attendee in similar_attendees:
            st.subheader("Attendee")
            st.write("**Name:** " + attendee['Name'])
            st.write("**Surname:** " + attendee['Surname'])
            st.write("**Email:** " + attendee['Email'])
            st.write("**Company:** " + attendee['Company'])
            st.write("**Job Title:** " + attendee['JobTitle'])

            interests = ""
            for interest in attendee['Interests']:
                interests = interests + interest + ", "
            st.write("**Interests:** " + interests)
            st.write(" ")