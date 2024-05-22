import streamlit as st
from streamlit_carousel import carousel
import src.creative_assistant_15 as app
st.session_state['show_text'] = False
st.set_page_config(
    layout="wide",
    page_title="👠 Creative Assistant",
    initial_sidebar_state="expanded",
)
st.title('👠 Creative Assistant')
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False
if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the idea of adopting a Platform instead of a single model. Use the model depending on your needs."
    how_to_use = "Select a model, enter a prompt, and choose the image style, camera effects, lens type, and image quality modifiers. Click on 'Generate images' to see the results."
    services_used = "Vertex AI, Imagen, StableDiffusion XL, Model Garden"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()


model = st.selectbox('Select a model', ['Imagen', 'StableDiffusion XL'])
initial_prompt = "breathtaking shot of a bag, luxury product style, elegant, sophisticated, high-end, luxurious, professional, highly detailed"
text_prompt = st.text_area('Enter your prompt here', height=200, value=initial_prompt)
col1, col2 = st.columns(2)
tags = []
with col1:
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        st.write('**Image style:**')
        image_style = st.radio('Choose an image style', ['None', 'Kodak Gold 200', 'Polaroid', 'Black and white', 'Lumix GH5', 'Film Noir'])
        st.write('**Camera effects:**')
        camera_effects = st.radio('Choose a camera effect', ['None', 'Bulb exposure', 'Close up', 'Fisheye', 'Soft focus', 'Motion blur'])
    with subcol2:
        st.write('**Lens type:**')
        lens_type = st.radio('Choose a lens type', ['None', '50mm', '35mm', '24mm', 'Telephoto'])
        st.write('**Image quality modifiers:**')
        image_quality = st.radio('Choose a quality modifier', ['None', 'High quality', '4K', 'HDR', 'Studio', 'Art'])
if st.button('Generate images'):    
    with col2:
        subcol1, subcol2 = st.columns(2)
        images = app.generate_images(model, text_prompt,image_style, camera_effects, lens_type, image_quality)
        i = 0
        for image_uniq in images:
            if i % 2 == 0:
                with subcol1:
                    st.image(image_uniq, use_column_width=True)
            else:
                with subcol2:
                    st.image(image_uniq, use_column_width=True)
            i += 1
        numbers = list(range(1, i+1))
        radio = st.radio('Select the best image', numbers, horizontal=True)

