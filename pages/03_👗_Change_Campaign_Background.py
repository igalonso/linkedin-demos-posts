import streamlit as st
import base64
from dotenv import load_dotenv
import src.change_campagin_background_03 as app

st.session_state['show_text'] = False
st.set_page_config(
    # page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="👗 Change Campaign Background",
    initial_sidebar_state="expanded",
)
st.title("👗 Change Campaign Background")
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo is a showcase of the capabilities of the Imagen model to generate background images for products. The user can select a product and the model will generate a background image based on the description of the product. The user can also select the creativity of the model."
    how_to_use = "Select the product you want to change the background to and click on the button to generate the background image. The model will generate a background image based on the description of the product. The user can also select the creativity of the model."
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown("Vertex AI, Model Garden, PaLM, Imagen")
    st.divider()

col1, col2 = st.columns(2)


with col1:
    #creativity = st.slider("Creativity", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    creativity = 0.5
    product = st.radio("Select a product: ", ("Jersey Cable Knit", "Cardigan 'Maureen'"))
    if product == "Jersey Cable Knit":
        st.image("assets/image1.jpeg", width=300)
        product_name = "Jersey Cable Knit"
        product_image = "assets/image1.jpeg"
        product_description = "A jersey for simple girls in their twenties that like to look comfortable"
    else:
        st.image("assets/image2.jpeg", width=300)
        product_name = "Cardigan 'Maureen'"
        product_image = "assets/image2.jpeg"
        product_description = "A cloth for winters days in the woods"

    if st.button("Generate Background Image for Springfield"):
        images = []
        in_file = open(product_image, "rb") # opening for [r]eading as [b]inary
        im = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
        prompt = "Generate a very descriptive prompt for a background image given a description. Never show people in the image \nHere is an example: \nDESCRIPTION: A woman jacket with patches of rock groups. \nPROMPT: A photo of a old pub in Ireland where the best rockbands play. Low lights and instruments in the background."
        prompt = prompt + "\nDESCRIPTION: " + product_description + " \nPROMPT: "
        print(prompt)
        st.write("**Description**: " + product_description)
        prompt = app.get_image_promt(prompt,creativity)
        st.write("**Generated Prompt:** " + prompt)
        images = app.generate_images(
            prompt=prompt,
            base_image=im,
            number_of_images=1,
            is_product_image=True,
        )
        num_photos = len(images)
        i = 0
        with col2: 
            subcol1, subcol2 = st.columns(2)
            for image in images:
                if i % 2 == 0:
                    with subcol1:
                        st.image(image, width=300)
                else:
                    with subcol2:
                        st.image(image, width=300)
                i = i + 1
            