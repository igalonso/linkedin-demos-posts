import subprocess
from dotenv import load_dotenv
import requests
import base64
import os
from PIL import Image
from io import BytesIO
import json
import vertexai


load_dotenv()
def get_access_token():
  access_token = subprocess.run(
      ["gcloud", "auth", "print-access-token"],
      capture_output=True,
      text=True,
  ).stdout.strip()

  if access_token.startswith("ya29"):
    return access_token
  else:
    raise Exception(
        f"Something went wrong with getting the access token."
        f"Restart the notebook and login again.\n {access_token}"
    )
def generate_payload_json(access_token, prompt, **kwargs):
  number_of_images = 4
  negative_prompt = kwargs.get("negative_prompt")
  image_size = kwargs.get("image_size")
  guidance_scale = kwargs.get("guidance_scale")
  seed = kwargs.get("seed")
#   base_image = kwargs.get("base_image")
  mask = kwargs.get("mask")
  mode = kwargs.get("mode")
  is_product_image = False

  headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json; charset=utf-8",
  }

  data = {
    "instances": [
      {
        "prompt": prompt
      }
    ],
    "parameters": {
      "sampleCount": number_of_images,
      "IsProductImage": True if is_product_image else None,
      "includeRaiReason": True,
      "includeSafetyAttributes": False
    }
  }

  return headers, json.dumps(data)


def send_request(headers, data):
  endpoint = os.environ["PREDICTION_ENDPOINT"]
  response = requests.post(endpoint, headers=headers, data=data)

  if response.status_code != 200:
    raise requests.exceptions.HTTPError(
        f"Error: {response.status_code} ({response.reason})")

  return response.json()


def generate_stable_diffusion_xl_images(text_prompt, image_style, camera_effects, lens_type, image_quality, **kwargs):
    # ...
    return "stable_diffusion_xl_images"

def generate_imagen_images(text_prompt, image_style, camera_effects, lens_type, image_quality, **kwargs):
    PROJECT_ID = os.environ["PROJECT_ID"]
    vertexai.init(project=PROJECT_ID, location="us-central1")
    # generation_model = TextGenerationModel.from_pretrained("text-unicorn")
    LOCATION = "us-central1"  # @param {type:"string"}
    IMAGE_MODEL_NAME = "imagegeneration@005"  # @param {type:"string"}
    BUCKET = ""  # @param {type:"string"}
    FOLDER = ""  # @param {type:"string"}
    CSV_FILE_NAME = ""  # @param {type:"string"}
    PREDICTION_ENDPOINT = (
        f"https://{LOCATION}-aiplatform.googleapis.com/v1/"
        f"projects/{PROJECT_ID}/locations/{LOCATION}/"
        f"publishers/google/models/{IMAGE_MODEL_NAME}:predict"
    )
    os.environ["PREDICTION_ENDPOINT"] = PREDICTION_ENDPOINT
    access_token = get_access_token()
    text_prompt += f" in {image_style} style"
    text_prompt += f" with {camera_effects} camera effect"
    text_prompt += f" using a {lens_type} lens"
    text_prompt += f" with {image_quality} quality"
    headers, data = generate_payload_json(access_token, text_prompt, **kwargs)
    response = send_request(headers, data)

    images = []
    if response:
        for pred in response["predictions"]:
            b64_decoded_string = base64.b64decode(pred["bytesBase64Encoded"])
            img = Image.open(BytesIO(b64_decoded_string))
            images.append(img)
        return images

def generate_images(model, text_prompt,image_style, camera_effects, lens_type, image_quality):
    if model == "Imagen":
        return generate_imagen_images(text_prompt, image_style, camera_effects, lens_type, image_quality)
    elif model == "StableDiffusion XL":
        return generate_stable_diffusion_xl_images(text_prompt, image_style, camera_effects, lens_type, image_quality)