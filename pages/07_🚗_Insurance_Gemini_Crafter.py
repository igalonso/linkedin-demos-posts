import streamlit as st
from PIL import Image
from src.insurace_gemini_crafter_07 import generate_insurance, add_mark_to_car, generate_insurance_fromjson
import cv2
import os

# Create two columns
st.header("Car Damage Insurance Estimator")

if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the capabilities of GenAI to provide a description of the damage based on a photo. The user can upload an image of a damaged car and the model will estimate the cost of the damage and provide a description of the damage."
    how_to_use = "Upload an image of a damaged car and the model will estimate the cost of the damage and provide a description of the damage."
    services_used = "Vertex AI, Model Garden, Gemini Pro Vision"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()

# st.subheader("Upload an image of a damaged car and get an estimate of the cost of the damage and a description of the damage.")
col1, col2 = st.columns(2)


# Add an image uploader to the first column
with col1:
    temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if uploaded_file is not None or st.button("Use example"):
        if uploaded_file is None:
            uploaded_file = "assets/crashcar.jpeg"
            st.text("Using example image")
        image = Image.open(uploaded_file)
        image = image.convert('RGB')
        image.save('crashcar.jpeg')
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        col2.empty()
        # Check if file exists then delete it
        if os.path.exists('marked_car.jpg'):
            os.remove('marked_car.jpg')
        else:
            print('File does not exist')
        with col2:
            with st.spinner('Reading and summarizing document...'):
                image_path = 'assets/crashcar.jpeg'
                response = generate_insurance(image_path, temp)
                # response = generate_insurance_fromjson(response)
                image_shape = cv2.imread('assets/car.jpeg')
                # Call the function
                marked_image = add_mark_to_car(image_shape, response)
                # Save the result
                cv2.imwrite('temp/marked_car.jpg', marked_image)
                st.image(marked_image, caption='Marked Image.', use_column_width=True)
                st.write("***Damaged parts:***")
                for part in response['damaged_parts']:
                    st.markdown("- "+ part)
                st.write("***Estimated cost:*** $"+str(response['estimated_cost']))
                with col1:
                    st.write(":red[Car Brand:] "+response["car_brand"])
                    st.write(":red[Car Model:] "+response["car_model"])
                    st.write(":red[Car Year:] "+response["car_year"])
                    st.write(":red[Description:] "+ response["description"])