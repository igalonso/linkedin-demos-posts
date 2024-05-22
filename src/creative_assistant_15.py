import subprocess
from dotenv import load_dotenv
import requests
import base64
import os
from PIL import Image
from io import BytesIO
import json
import vertexai
from google.cloud import aiplatform
from typing import Dict, List, Union
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

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

def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "europe-west1",
    api_endpoint: str = "europe-west1-aiplatform.googleapis.com",
):
    # The pre-built serving docker image. It contains serving scripts and models.
    SERVE_DOCKER_URI = "us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-diffusers-serve-opt:20240223_1230_RC00"
    aiplatform.init(project="gen-ai-igngar", location="europe-west1", staging_bucket="sd-igngar-bucket")
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = instances if isinstance(instances, list) else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    predictions = response.predictions
    # for prediction in predictions:
    #     print(" prediction:", dict(prediction))
    return predictions


def generate_stable_diffusion_xl_images(text_prompt, image_style, camera_effects, lens_type, image_quality, **kwargs):
    # ...
    if image_style != "None":
       text_prompt += f", {image_style}"
    if camera_effects != "None":
      text_prompt += f", {camera_effects}"
    if lens_type != "None":
      text_prompt += f", {lens_type} lens"
    if image_quality != "None":
      text_prompt += f", {image_quality}"
    print(f"FINAL PROMPT: {text_prompt}")
    endpoint = os.environ["CUSTOM_STABLE_ENDPOINT"]
    project_id = os.environ["CUSTOM_PROJECT_ID"]
    sample =  [
                {
                        "prompt": text_prompt,
                        "num_inference_steps": 50,
                }
        ]
    i = 0
    images = []
    while i < 4:
      result = predict_custom_trained_model_sample(project_id,endpoint,sample)
      image_data = result[0]
      image_bytes = base64.b64decode(image_data)
      img = Image.open(BytesIO(image_bytes))
      images.append(img)
      i += 1
    return images

def generate_imagen_images(text_prompt, image_style, camera_effects, lens_type, image_quality, **kwargs):
    PROJECT_ID = os.environ["PROJECT_ID"]
    vertexai.init(project=PROJECT_ID, location="us-central1")
    # generation_model = TextGenerationModel.from_pretrained("text-unicorn")
    LOCATION = "us-central1"  # @param {type:"string"}
    IMAGE_MODEL_NAME = "imagegeneration@006"  # @param {type:"string"}
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
    


