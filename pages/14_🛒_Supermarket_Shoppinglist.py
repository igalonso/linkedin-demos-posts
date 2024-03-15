
import streamlit as st
import src.supermarket_shoppinglist_14 as  app
from PIL import Image
st.set_page_config(layout='wide')
max_items = 6

# @st.cache_data(show_spinner=False)
def retrieve_alternative_list(shopping_list):
    
    index = 0
    alternatives = []   
    for item_wanted in shopping_list:
        if index == max_items:
            break
        item_product = item_wanted["product"]
        alternatives_list = app.retrieveProductAlternatives(item_product)
        alternatives.append(alternatives_list)
        index += 1
    return alternatives
st.header("📝 Share your shopping list!")

if 'show_text' not in st.session_state:
    st.session_state['show_text'] = False

if st.button('Instructions'):
    # Toggle the state when button is clicked
    st.session_state['show_text'] = not st.session_state['show_text']

# Only show the text if the state is True
if st.session_state['show_text']:
    st.markdown("**Purpose of demo:**")
    explanation = "This demo showcases the multimodal capabilities of Gemini. The use uploads a photo of a shopping list and the model will provide alternatives for the products in the shopping list. The model queries Vertex Search with BigQuery as a datastore. We Used BigQueryML to generate categories on each product"
    how_to_use = "Upload a photo of a shopping list and the model will provide alternatives for the products in the shopping list. Select the different products for each item and show that, when we don't have the product in stock, we can't provide alternatives and states it."
    services_used = "Vertex AI, Gemini Pro Vision, Vertex Search, BigQuery"
    st.markdown(f'<span style="word-wrap:break-word;">{explanation}</span>', unsafe_allow_html=True)
    st.markdown("**How to use the demo:**")
    st.markdown(f'<span style="word-wrap:break-word;">{how_to_use}</span>', unsafe_allow_html=True)
    st.markdown("**Services used:**")
    st.markdown(services_used, unsafe_allow_html=True)
    st.divider()


# Create the main layout of the web page
main_col1, main_col2, main_col3= st.columns(3)
with main_col3:
    st.header("🛒 Shopping cart")
    st.write("This is your shopping cart.")
# Populate the first column
with main_col1:
    # picture = st.camera_input("Show me your shopping list:")
    
    # picture = st.camera_input("Show me your shopping list:")
    picture = st.file_uploader("Show me your shopping list:")
    if picture:
        st.image(picture, caption='Uploaded Image.', use_column_width=True)
        image = Image.open(picture)
        image = image.convert('RGB')
        image.save('list.jpeg')
        shopping_list = app.retrieveShoppingList(picture)["products"]
        with main_col2:
            st.subheader("🤖 This is what we read from your shopping list:")
            st.write("We only show the first 5 items from your shopping list.")
            alternatives = retrieve_alternative_list(shopping_list)
            
            index = 0
            for item in shopping_list:
                if index == max_items:
                    break
                alternative_names = []
                alternatives_list = alternatives[index]
                item_product = item["product"]
                if alternatives_list == []:
                    with main_col1:
                        st.write(f"I see that you added {item_product} to your shopping list. We don't have this product in our stock.")
                    index += 1
                    continue
                else:
                    for alternative in alternatives_list:
                        product_title = alternative["name"] + " " + alternative["brand"]
                        alternative_names.append(product_title)
                    option = st.radio(f"I see that you added {item_product} to your shopping list. Which one from our stock?",alternative_names, horizontal=True, index=0)
                    st.image(alternatives_list[alternative_names.index(option)]["img_url"], caption=option, width=100)
                    index += 1
                    if st.button(f"Add to {option} shopping cart"):
                        with main_col3:
                            st.image(alternatives_list[alternative_names.index(option)]["img_url"], caption=option, width=100)
                            st.write(f"{option} added to shopping cart.")

