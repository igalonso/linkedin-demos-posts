import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold, Tool
from vertexai.preview import generative_models

import cv2
import numpy as np
import json
from PIL import Image
import io

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

def generate_insurance(image_path, temperature=0):
    image1=Part.from_data(data=base64.b64decode(get_image_base64(image_path)), mime_type="image/jpeg")
    json_format = {
        "hit":[{
            "position": "one or many of these values - front-left, front, front-right, middle-left, middle-top, middle-right, bottom-left, bottom, bottom-right",
            "damage": "one of these values - high, mid, low or none"
            }],
        "description": "description of the damage starting always with the phrase 'From the point of view of the person taking the picture",
        "damaged_parts": ["a list of damaged parts of the car"],
        "estimated_cost": "estimated cost of the damage in dollars. This is a float type number",
        "car_brand": "car brand",
        "car_model": "car model",
        "car_year": "car year in string format"
    }
    prompt = f"You are an insurace agent. Describe me the positions, and severities of the different zones of damage of this car. When a visible damage is seen, it should be, at least, low. If damage is noticeable, it should be high. Give me the response using this json format: {json_format} using double quotes without ```json. JSON:"
       
    model = GenerativeModel("gemini-pro-vision")
    responses = model.generate_content(
        [image1, prompt],
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
    return json.loads(responses.candidates[0].content.parts[0].text)


#definition of function to "use Vertex AI Function calling. Still on progress and not used in the UI"
def generate_insurance_fromjson(json_response):
    prompt = f"You are an insurace agent. Describe me the positions, and severities of the different zones of damage of this car based on this json {json_response} using double quotes without ```json. JSON:"
    model = GenerativeModel("gemini-pro")
    claim_spec = {
        'name':'get_current_claim',
        'description':'Fullfill the documentation on a claim based on the information from the photo',
        'parameters':{
            'type': 'object',
            'properties':{
                'hit':{
                    'type': 'array',
                    'description': 'a list of hits',
                    'items':{
                        'type': 'object',
                        'properties':{
                            'position':{
                                'type': 'string',
                                'enum': ['front-left', 'front', 'front-right', 'middle-left', 'middle-top', 'middle-right', 'bottom-left', 'bottom', 'bottom-right'],
                                'description': 'one or many of these values - front-left, front, front-right, middle-left, middle-top, middle-right, bottom-left, bottom, bottom-right'
                            },
                            'damage':{
                                'type': 'string',
                                'enum': ['high', 'mid', 'low', 'none'],
                                'description': 'one of these values - high, mid, low or none'
                            
                            }
                        }
                    }
                },
                'description':{
                    'type': 'string',
                    'description': 'description of the damage starting always with the phrase "From the point of view of the person taking the picture"'
                },
                'damaged_parts':{
                    'type': 'array',
                    'description': 'a list of damaged parts of the car',
                    'items':{
                        'type': 'string',
                        'description': 'a damaged part of the car'
                    }
                },
                'estimated_cost':{
                    'type': 'number',
                    'description': 'estimated cost of the damage in dollars. This is a float type number'
                },
                'car_brand':{
                    'type': 'string',
                    'description': 'car brand'
                },
                'car_model':{
                    'type': 'string',
                    'description': 'car model'
                },
                'car_year':{
                    'type': 'string',
                    'description': 'car year in string format'
                }
            },
            'required': [
                'hit','description','damaged_parts','estimated_cost','car_brand','car_model','car_year'
            ]
        }
    }
    all_tools = Tool.from_dict(
        {
            "function_declarations": [claim_spec]
        }
    )
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 1,
        "top_k": 32
    }
    response = model.generate_content(
        prompt,
        generation_config=generation_config,
        tools=[all_tools],
    )
    print(response)
    return response

def add_mark_to_car(image,response):
    # Define the color based on the severity
    for hit in response['hit']:
        severity = hit['damage']
        position = hit['position']
        if severity == 'high':
            color = (255, 0, 0)
        elif severity == 'mid':
            color = (255, 128, 0)
        elif severity == 'low':
            color = (255, 255, 0)   
        elif severity == 'none':
            break

        # Define the position based on the position string
        height, width, _ = image.shape
        positions = {
            'front-right': (int(width * 0.08), int(height * 0.05)),
            'front': (int(width * 0.5), int(height * 0.05)),
            'front-left': (int(width * (1-0.08)), int(height * 0.05)),
            'middle-right': (int(width * 0.08), int(height * 0.5)),
            'middle-top': (int(width * 0.5), int(height * 0.5)),
            'middle-left': (int(width * (1-0.08)), int(height * 0.5)),
            'bottom-right': (int(width * 0.08), int(height * (1-0.05))),
            'bottom': (int(width * 0.5), int(height * (1-0.05))),
            'bottom-left': (int(width * (1-0.08)), int(height * (1-0.05))),
        }
        pos = positions.get(position, (0, 0))

        # Draw a circle at the position with the color
        cv2.circle(image, pos, 30, color, -1)

    return image