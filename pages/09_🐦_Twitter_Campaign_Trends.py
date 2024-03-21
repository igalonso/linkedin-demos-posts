import streamlit as st
import base64
from dotenv import load_dotenv
import src.twitter_campaign_trends_09 as app


st.set_page_config(
    # page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="🐦 Fast X Campaigns",
    initial_sidebar_state="expanded",
)
st.title("🐦 Fast X Campaigns")
if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the capabilities of the GenAI to create campaigns for products based on recent information from Twitter. The user can select a product and a trending topic and the model will generate a tweet for the campaign."
    how_to_use = "Select a product and a trending topic and click on the button to create a campaign tweet. The model will generate a tweet for the campaign based on the product and the trending topic."
    services_used = "Vertex AI, Gemini Pro Vision, Imagen, Fake Twitter API"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()

col1, col2, col3 = st.columns(3)


if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False






products =[{"name":"iPhone 15 Pro","image":"assets/iphone.png", "description":"The iPhone 15 Pro is the best iPhone ever. It has a 6.7 inch screen, 5G, and a 120Hz refresh rate. It also has a 50MP camera, 8K video recording, and a 5000mAh battery."},{"name":"Samsung Galaxy S23 Ultra","image":"assets/samsung.png", "description":"The Samsung Galaxy S23 Ultra is a flagship Android smartphone unveiled in February 2023. It boasts a powerful processor, a versatile camera system, and a large, high-resolution display."},{"name":"Google Pixel 8 Pro","image":"assets/google.png", "description":"The Google Pixel 8 Pro is a flagship Android smartphone It boasts a powerful processor, a versatile camera system, and a large, high-resolution display."}]

with col1:
    st.subheader("Select a product")
    product = st.radio("Select a product: ", ("iPhone 15 Pro", "Samsung Galaxy S23 Ultra", "Google Pixel 8 Pro"))
    if product == "iPhone 15 Pro":
        st.image(products[0]["image"], width=75)
        product_name = products[0]["name"]
        product_image = products[0]["image"]
        product_description = products[0]["description"]  
    elif product == "Samsung Galaxy S23 Ultra":
        st.image(products[1]["image"], width=75)
        product_name = products[1]["name"]
        product_image = products[1]["image"]
        product_description = products[1]["description"]  
    else:
        st.image(products[2]["image"], width=75)
        product_name = products[2]["name"]
        product_image = products[2]["image"]
        product_description = products[2]["description"]  
    trends = app.gather_twitter_current_local_trends()
    trends_str =[]
    for trend in trends["data"]:
        trends_str.append(trend["trend_name"]) 
    trend = st.radio("Select a trending topic: ", trends_str)
    if st.button("Create campaign tweet"):
        tweet = app.get_copy_from_trend(trend,product_name, product_description)
        with col2:
            st.subheader("Campaign Tweet")
            st.write("Body: " + tweet["body"])
            st.write("Hashtags: " + tweet["hashtags"])
            st.write("Link: " + tweet["link"])
            st.write("Features: " + tweet["features"])
            st.write("Call To Action: " + tweet["call_to_action"])
            st.write("Aditional Notes: " + tweet["additional_notes"])
            st.write("Background notes prompt: " + tweet["background_image"])

        with col3:
            app.generate_image_from_tweet(tweet["background_image"],product_image)
            app.generate_photo("Easy Mobile", "@easy_mobile_shop", tweet["body"], tweet["hashtags"], tweet["link"], "assets/user_photo.png", "assets/output.png")
            st.image("assets/output_tweet.png", width=400)
