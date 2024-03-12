import streamlit as st
from PIL import Image
from src.insurace_gemini_crafter_07 import generate_insurance, add_mark_to_car, generate_insurance_fromjson
import cv2
import os

# Create two columns
st.header("Car Damage Insurance Estimator")
st.subheader("Upload an image of a damaged car and get an estimate of the cost of the damage and a description of the damage.")
col1, col2 = st.columns(2)


# Add an image uploader to the first column
with col1:
    temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if uploaded_file is not None:
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