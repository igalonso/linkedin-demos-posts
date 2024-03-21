import streamlit as st
import base64
from dotenv import load_dotenv
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '')

from src.ER_triage_demo_05 import *
import os
import json

load_dotenv()
if __name__ == "__main__":
    pass
patient_1 = os.environ["PATIENT_ID_1"]
patient_2 = os.environ["PATIENT_ID_2"]
patient_3 = os.environ["PATIENT_ID_3"]
patient_1_symptoms = os.environ["PATIENT_SYMPTOMS_1"]
patient_2_symptoms = os.environ["PATIENT_SYMPTOMS_2"]
patient_3_symptoms = os.environ["PATIENT_SYMPTOMS_3"]
patients = os.environ["NUM_PATIENTS_ER"]
max_patients = os.environ["MAX_PATIENTS_ER"]


def get_colors(severity):
    if severity == "Low":
        return ":green["
    elif severity == "Medium":
        return ":orange["
    elif severity == "High":
        return ":red["
    else:
        return ":grey["

st.set_page_config(
    # page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="🏥 ER Room Triage",
    initial_sidebar_state="expanded",
)
st.title("🏥 ER Room Triage")

if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the capabilities of the GenAI to build triage services. The user can select the number of patients in the ER and the model will triage the patients based on their symptoms. The model will also provide a reasoning for the triage level."
    how_to_use = "Select the number of patients in the ER and click on the button to triage the patients. The model will triage the patients based on their symptoms from Healthcare API. The model will also provide a reasoning for the triage level."
    services_used = "Vertex AI, Model Garden, Healthcare API"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()

col1, col2, col3 = st.columns(3)


with col1:
    st.image("assets/patient.png", width=75)
    if st.button("Enter the room", key="Patient 1"):
        with col3:
            col3.empty() 
            st.subheader("Patient 1")
            st.write("**Patient ID:** "+ patient_1)
            st.write("**Patient Symptoms:** "+ patient_1_symptoms)
            result = json.loads(triage_patient(patient_1_symptoms,patient_1,max_patients,patients))
            st.write("**Triage Level:** "+ get_colors(result["triage_level"])+result["triage_level"]+"]")
            st.write("**Reasoning:** "+ result["reasoning"])
            st.write("**Patient History:** "+ result["patient_history"])         
               
    st.image("assets/patient.png", width=75)
    if st.button("Enter the room", key="Patient 2"):
        with col3:
            col3.empty() 
            st.subheader("Patient 2")
            st.write("**Patient ID:** "+ patient_2)
            st.write("**Patient Symptoms:** "+ patient_2_symptoms)
            result = json.loads(triage_patient(patient_2_symptoms,patient_2,max_patients,patients))
            st.write("**Triage Level:** "+ get_colors(result["triage_level"])+result["triage_level"]+"]")
            st.write("**Reasoning:** "+ result["reasoning"])
            st.write("**Patient History:** "+ result["patient_history"]) 
    
    st.image("assets/patient.png", width=75)
    if st.button("Enter the room", key="Patient 3"):
        with col3:
            col3.empty() 
            st.subheader("Patient 3")
            st.write("**Patient ID:** "+ patient_3)
            st.write("**Patient Symptoms:** "+ patient_3_symptoms)
            result = json.loads(triage_patient(patient_3_symptoms,patient_3,max_patients,patients))
            st.write("**Triage Level:** "+ get_colors(result["triage_level"])+result["triage_level"]+"]")
            st.write("**Reasoning:** "+ result["reasoning"])
            st.write("**Patient History:** "+ result["patient_history"])  
    
with col2:
    st.image("assets/er.png")
    patients = st.number_input("# Patients in ER", min_value=0, max_value=5, value=0, step=1, key="patients")
    st.subheader("Max ER Capacity: "+ str(max_patients))
