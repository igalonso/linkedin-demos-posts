import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold, Tool
import vertexai.preview.generative_models as generative_models
from dotenv import load_dotenv
import os
import json
from PIL import Image
import io
from langchain_community.retrievers import GoogleVertexAISearchRetriever
from langchain_community.llms import VertexAI
from langchain.chains import RetrievalQA
import streamlit as st

load_dotenv()
if __name__ == "__main__":
    pass

def get_image_base64(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Create a BytesIO object
        with io.BytesIO() as buf:
            # Save the image to the BytesIO object
            img.save(buf, format='PNG')
            # Get the byte data
            byte_data = buf.getvalue()
            # Convert the byte data to base64
            base64_data = base64.b64encode(byte_data)
            # Decode the base64 to get a string
            base64_string = base64_data.decode('utf-8')

    return base64_string

def get_product_query(query: str):
    retriever = GoogleVertexAISearchRetriever(
        project_id=os.environ["PROJECT_ID"],
        location_id=os.environ["LOCATION_ID"],
        data_store_id=os.environ["DATA_STORE_ID"],
        max_documents=3,
        engine_data_type=1,
    )
    result = retriever.get_relevant_documents(query)
    print(result)
    return result

@st.cache_data(show_spinner=False)
def retrieveShoppingList(image_path):
    vertexai.init(project="gen-ai-igngar", location="us-central1")
    image=Part.from_data(data=base64.b64decode(get_image_base64(image_path)), mime_type="image/jpeg")
    model = GenerativeModel("gemini-1.0-pro-vision-001")
    json_format = {
        "products": [{"product": "product name", "quantity": "quantity"}]
    }
    project_id = os.environ.get("PROJECT_ID")
    prompt = f"Give me the list of items I want to buy at the supermarket in English. Use the following json format: {json_format} using double quotes"
    
    temperature = 0.5
    model = GenerativeModel("gemini-pro-vision")
    responses = model.generate_content(
        [image, prompt],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": temperature,
            "top_p": 1,
            "top_k": 32
        },
        stream = False,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    shopping_list= responses.candidates[0].content.parts[0].text
    shopping_list = shopping_list.replace('```json', '')
    shopping_list = shopping_list.replace('```', '')
    # print(shopping_list)
    return json.loads(shopping_list)
@st.cache_data(show_spinner=False)
def retrieveProductAlternatives(shoppingListItem):
    print("-------")
    print(shoppingListItem)
    products = get_product_query(shoppingListItem)
    alternatives = []
    id = 0
    for doc in products:
        name = json.loads(doc.page_content)["name"]
        price = json.loads(doc.page_content)["price"]
        currency = json.loads(doc.page_content)["currency"]
        brand = json.loads(doc.page_content)["brand"]
        id = json.loads(doc.page_content)["id"]
        img_url = json.loads(doc.page_content)["image_url"]
        alternatives.append({"name": name, "price": price, "currency": currency, "brand": brand, "id": id, "img_url": img_url})
    print(alternatives)
    print("-------")
    return alternatives