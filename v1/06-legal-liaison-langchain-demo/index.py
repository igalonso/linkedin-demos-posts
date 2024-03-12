import streamlit as st
from app import text_summarization,summarize_pdf
import os
import shutil
import base64

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
    page_title="Legal liaison companion",
    initial_sidebar_state="expanded",
)


st.markdown(
    # f'<div class="header"><figure><embed type="image/svg+xml" src="web/img/sdr.svg" /><figcaption></figcaption></figure><h3> React Agents Demo with Vertex AI (Google Cloud) </h3></div>',
    f"<div class='header'><h3> Leagal liason document summarization </h3></div>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    method_type = st.radio("***Select a method to summarize***", ("Map Reduce", "Refine"),captions = ["Map reduce method to summarize", "Alternative refine method based on mapreduce"])
    if method_type == "Map Reduce":
        method_type = "map_reduce"
    elif method_type == "Refine":
        method_type = "refine"
    challenge = st.text_input("***What is the challenge you are facing?***")
    uploaded_file = st.file_uploader("***Which file would you like to summarize?***")
    
    if uploaded_file is not None:
        col2.empty()
        with open(os.path.join('data', uploaded_file.name), 'wb') as f:
            shutil.copyfileobj(uploaded_file, f)
        st.success("Saved File")
        with col2:
            with st.spinner('Reading and summarizing document...'):    
                displayPDF("data/" + uploaded_file.name)
                # formal_summary = read_and_formally_summarize_text("data/" + uploaded_file.name)
                formal_summary = summarize_pdf("data/" + uploaded_file.name, method_type)
                summary = text_summarization(formal_summary,challenge)
                st.write("\n\n:red[Simple Summary]")
                st.write(summary)

        




