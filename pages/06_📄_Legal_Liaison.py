import streamlit as st
from src.legal_liaison_06 import text_summarization,summarize_pdf
import os
import shutil
import base64
st.session_state['show_text'] = False
def get_colors(severity):
    if severity == "Low":
        return ":green["
    elif severity == "Medium":
        return ":orange["
    elif severity == "High":
        return ":red["
    else:
        return ":grey["

def displayPDF(uploaded_file):
    with open(uploaded_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="450" height="500" type="application/pdf"></iframe>'
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(
    # page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="📄 Legal liason document summarization",
    initial_sidebar_state="expanded",
)
st.title("📄 Legal liason document summarization")

if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the capabilities of GenAI to summarize legal documents. The user can upload a legal document and the model will summarize the document based on the method selected."
    how_to_use = "Select a method to summarize the document, a challenge you might be facing (i.e. 'I want to be explained for a 10 years old.') and click on the button to summarize the document. The model will summarize the document based on the method selected."
    services_used = "Vertex AI, Model Garden, Gemini, Document AI"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()

col1, col2 = st.columns(2)

with col1:
    method_type = st.radio("***Select a method to summarize***", ("Map Reduce", "Refine"),captions = ["Map reduce method to summarize", "Alternative refine method based on mapreduce"], index=1)
    if method_type == "Map Reduce":
        method_type = "map_reduce"
    elif method_type == "Refine":
        method_type = "refine"
    challenge = st.text_input("***What is the challenge you are facing?***", "I want to be explained for a 10 years old.")
    uploaded_file = st.file_uploader("***Which file would you like to summarize?***")
    with open("assets/06_legal_liaison.pdf", "rb") as file:
        btn = st.download_button(
            label="Download sample pdf",
            data=file,
            file_name="06_legal_liaison.pdf",
            mime="application/pdf"
        )
    if uploaded_file:
        col2.empty()
        with open(os.path.join('temp', uploaded_file.name), 'wb') as f:
            shutil.copyfileobj(uploaded_file, f)
            st.success("Saved File")
        with col2:
            with st.spinner('Reading and summarizing document...'):    
                displayPDF("temp/" + uploaded_file.name)
                # formal_summary = read_and_formally_summarize_text("data/" + uploaded_file.name)
                formal_summary = summarize_pdf("temp/" + uploaded_file.name, method_type)
                summary = text_summarization(formal_summary,challenge)
                st.write("\n\n:red[Simple Summary]")
                st.write(summary)
   

        




