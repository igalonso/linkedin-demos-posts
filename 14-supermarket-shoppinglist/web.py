
import streamlit as st
import app
from PIL import Image
from streamlit_carousel import carousel
st.set_page_config(layout='wide')

# Create the main layout of the web page
main_col1, main_col2= st.columns(2)
with main_col2:
    st.header("Column 2")
    st.write("This is column 2.")
# Populate the first column
with main_col1:
    st.header("Column 1")
    st.write("This is column 1.")
    # picture = st.camera_input("Show me your shopping list:")
    picture = st.file_uploader("Show me your shopping list:")
    if picture:
        st.image(picture, caption='Uploaded Image.', use_column_width=True)
        image = Image.open(picture)
        image = image.convert('RGB')
        image.save('list.jpeg')
        shopping_list = app.retrieveShoppingList(picture)["products"]
        i = 0
        with main_col2:
            for item in shopping_list:
                item_product = item["product"]
                alternatives_list, id = app.retrieveProductAlternatives(item_product)
                if id == 0:
                    st.write(f"I see that you added {item_product} to your shopping list. We don't have this product in our stock.")
                else:
                    items = []
                    for alternative in alternatives_list:
                        brand = alternative["brand"]
                        price = alternative["price"]
                        currency = alternative["currency"]
                        id = alternative["id"]
                        name = alternative["name"]
                        img_url = alternative["img_url"]

                        items.append(dict(
                            title=name,
                            text=f"{brand} @ {price} {currency}",
                            img=img_url,
                        ))
                    carousel(items=items, width=1)
                    # option = st.selectbox(f"I see that you added {item_product} to your shopping list. Which one from our stock?",(alternatives_list), key=f"{id}-{item_product}")



