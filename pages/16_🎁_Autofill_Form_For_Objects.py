import streamlit as st
from PIL import Image
import src.autofill_form_for_objects_16 as  app

st.session_state['show_text'] = False
st.set_page_config(
    layout="wide",
    page_title="🎁 Autofill Form For Objects",
    initial_sidebar_state="expanded",
)
st.title('🎁 Autofill Form For Objects')
if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False
if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the multimodal capabilities to enhance marketplaces sellers experience by autofilling forms for objects."
    how_to_use = "Upload an image and see the form autofilled with the object's details."
    services_used = "Vertex AI, Gemini Pro Vision"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()

# Create the main layout of the web page
main_col1, main_col2= st.columns(2)
with main_col1:
    picture = st.file_uploader("Upload a photo of your shopping list", type=["jpg", "jpeg", "png"])
    with open("assets/objeto_de_compra.jpeg", "rb") as file:
        btn = st.download_button(
            label="Download sample image",
            data=file,
            file_name="objeto_de_compra.jpeg",
            mime="image/jpeg"
        )
    if picture: 
        image = Image.open(picture)
        st.image(image, caption="Uploaded image", use_column_width=True)
        
        with main_col2: 
            image = image.convert('RGB')
            image.save('image_object.jpg')
            suggestions = app.autofill_form_for_objects(picture)
            conditions = ['New','Slightly used','Used','Heavy used','Refurbished','For parts','Not working']
            proposed_price = app.retrieve_proposed_price(suggestions['product'], suggestions['brand'],suggestions['model'],suggestions['condition'])
            if proposed_price == 0:
                proposed_price = suggestions['price']
            st.text_input("Product Name",value=suggestions['product'])
            st.text_area("Description",value=suggestions['description'])
            st.text_input("Category",value=suggestions['category'])
            st.text_input("Brand",value=suggestions['brand'])
            st.text_input("Model",value=suggestions['model'])
            st.text_input("Year",value=suggestions['year'])
            st.selectbox("Condition",conditions,index=conditions.index(suggestions['condition']))
            st.text_input("Color",value=suggestions['color'])
            st.text_area("Reason for selling",value=suggestions['reason_for_selling'])
            st.slider("Price", min_value=1.0, max_value=float(proposed_price)*3, value=float(proposed_price))
            st.selectbox("Negotiable",['Yes','No'],index=0 if suggestions['negotiable']=='yes' else 1)
            st.selectbox("Delivery",['Yes','No'],index=0 if suggestions['delivery']=='yes' else 1)





    