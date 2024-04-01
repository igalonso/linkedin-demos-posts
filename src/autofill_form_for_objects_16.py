from vertexai.preview.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold
import json
import base64
from PIL import Image
import io
from langchain_community.retrievers import GoogleVertexAISearchRetriever
import os
from dotenv import load_dotenv


load_dotenv()
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

def retrieve_categories():
    categories = ["Cars", "Motorcycles", "Motorcycles and Accessories", "Fashion and Accessories", "Real Estate", "Technology and Electronics", "Movies and Telephony", "Informatics", "Sports and Hobbies", "Bicycles", "Consoles and Video Games", "Home and Garden", "Household Appliances", "Cinema, Books and Music", "Children and Babies", "Construction and Reforms", "Industry and Agriculture", "Employment", "Services", "Others"]
    return categories

def get_product_query(query: str):
    retriever = GoogleVertexAISearchRetriever(
        project_id=os.environ["PROJECT_ID"],
        location_id=os.environ["LOCATION_ID"],
        data_store_id=os.environ["SECONDHAND_DATA_STORE_ID"],
        max_documents=3,
        engine_data_type=1,
    )
    result = retriever.get_relevant_documents(query)
    return result


def autofill_form_for_objects(image_path):

    image=Part.from_data(data=base64.b64decode(get_image_base64(image_path)), mime_type="image/jpeg")
    conditions = ['New','Slightly used','Used','Heavy used','Refurbished','For parts','Not working']
    categories = retrieve_categories()
    json_format= {
        "product": "product name",
        "description": "description of the second hand object. This description should not be a marketing one but a user description of the object.",
        "category": f"category of the object from one of these: {categories}",
        "brand": "brand",
        "model": "model",
        "year": "year",
        "price": "price in USD",
        "condition": f"condition from one of these:{conditions}",
        "color": "color",
        "reason_for_selling": "reason for selling",
        "negotiable": "yes/no",
        "delivery": "yes/no",
        "location": "location",
        "contact": "contact",
    }
    prompt = f"You are an agent that suggests the user to fill a form with the details of the object in the image. Use the following json format to return the answer sing double quotes\nJSON_FORMAT:\n{json_format}\nANSWER:" 
    temperature = 0
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

    object_suggestions= responses.candidates[0].content.parts[0].text
    object_suggestions = object_suggestions.replace('```json', '')
    object_suggestions = object_suggestions.replace('```', '')
    # print(shopping_list)
    return json.loads(object_suggestions)

def retrieve_proposed_price(product, brand, model, condition):
    # This is a placeholder function that returns a proposed price based on the product, brand, model, and condition
    query = f"{product} {brand} {model} {condition}"
    products = get_product_query(query)
    prices = []
    for product in products:
        print(product.page_content)
        prices.append(json.loads(product.page_content)["Price"])

    if prices:
        return sum(prices) / len(prices)
    else:
        return 0