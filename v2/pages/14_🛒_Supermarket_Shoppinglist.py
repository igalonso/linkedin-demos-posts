
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


# Create the main layout of the web page
main_col1, main_col2, main_col3= st.columns(3)
with main_col3:
    st.header("🛒 Shopping cart")
    st.write("This is your shopping cart.")
# Populate the first column
with main_col1:
    # picture = st.camera_input("Show me your shopping list:")
    st.header("📝 Share your shopping list!")
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

