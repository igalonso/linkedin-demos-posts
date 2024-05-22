import streamlit as st

st.session_state['show_text'] = False
st.set_page_config(
    page_title="oneweekoneusecase",
    page_icon="👋",
)
st.write("# Hello LinkedIn Fam! 👋")
st.sidebar.success("Select a demo above.")
# Initialize the session state if it doesn't exist
st.text("👈🏼 Select a demo from the left panel to get started!")
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown(
        """
        This is a space where you can test all of the demos I've created!\n
        """)
    st.image("assets/intro.png")
    
    st.markdown(
        """
        In the left panel you will see all the demos available.\n
        To test them out, go to this link and select the resources to be used on each demo. [go link](http://go/oneweekoneusecase)\n
        Find the best resources with the name of the demo on each of them. \n
        Of course, feel free to test them with your own resources as well but keep in mind that the results may vary (or not!).\n
        It is only for demo purposes, so retry if it fails, don't shot the messenger!😅\n
        And, of course, if you have any questions, feel free to reach out to me!\n

        To follow me on LinkedIn, click [here](https://www.linkedin.com/in/igngar) and get all the new demos every week \n
        [igngar@](https://moma.corp.google.com/person/igngar) - Nacho Garcia

    """
    )