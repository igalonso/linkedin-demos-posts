import pandas as pd
import seaborn as sns
from vertexai.language_models import TextGenerationModel, \
                                     TextEmbeddingModel, \
                                     ChatModel, \
                                     InputOutputTextPair, \
                                     CodeGenerationModel, \
                                     CodeChatModel
from vertexai.vision_models import ImageTextModel
from google.cloud import storage
import csv
# @title
import base64
import json
import os
import requests
import subprocess
from io import BytesIO

from PIL import Image

from io import BytesIO
import vertexai
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    pass


def get_access_token():
  """Gets the access token from the Google Cloud SDK.

  Returns:
    The access token.

  Raises:
    Exception: If something went wrong with getting the access token.
  """

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
  """Generates the JSON data for the API request.

  Args:
    access_token: The access token for the API.
    prompt: The prompt for the image generation.
    **kwargs: Optional parameters for the API request.

  Returns:
    A tuple of the headers and the JSON data.
  """

  number_of_images = kwargs.get("number_of_images")
  negative_prompt = kwargs.get("negative_prompt")
  image_size = kwargs.get("image_size")
  guidance_scale = kwargs.get("guidance_scale")
  seed = kwargs.get("seed")
  base_image = kwargs.get("base_image")
  mask = kwargs.get("mask")
  mode = kwargs.get("mode")
  is_product_image = kwargs.get("is_product_image")

  headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json; charset=utf-8",
  }

  data = {
    "instances": [
      {
        "prompt": prompt,
        "image": {
            "bytesBase64Encoded": base64.b64encode(base_image).decode("ascii")
         }
      }
    ],
    "parameters": {
      "negativePrompt": negative_prompt,
      "sampleCount": number_of_images,
      "sampleImageSize": image_size,
      "seed": seed,
      "guidanceScale": guidance_scale,
      "IsProductImage": True if is_product_image else None,
      "includeRaiReason": True,
      "includeSafetyAttributes": False
    }
  }

  return headers, json.dumps(data)


def send_request(headers, data):
  """Sends a POST request to the specified endpoint.

  Args:
    headers: A dictionary of headers to include in the request.
    data: The data to send in the request body.

  Returns:
    The JSON response from the endpoint.

  Raises:
     requests.exceptions.HTTPError: If the status code of the response is not 200.
  """
  endpoint = os.environ["PREDICTION_ENDPOINT"]
  response = requests.post(endpoint, headers=headers, data=data)

  if response.status_code != 200:
    raise requests.exceptions.HTTPError(
        f"Error: {response.status_code} ({response.reason})")

  return response.json()


def generate_images(prompt, **kwargs):
  """Generates images from the prompt.

  Args:
    prompt: The prompt to generate images from.
    **kwargs: Keyword arguments to pass to the prediction API.

  Returns:
    A list of Image objects.
  """
  access_token = get_access_token()
  headers, data = generate_payload_json(access_token, prompt, **kwargs)
  response = send_request(headers, data)

  images = []
  if response:
    for pred in response["predictions"]:
      b64_decoded_string = base64.b64decode(pred["bytesBase64Encoded"])
      img = Image.open(BytesIO(b64_decoded_string))
      images.append(img)
    return images


def show_images(images):
  """Shows images in a grid.

  Args:
    images: A list of Image objects.
  """

  nrows = 2 if len(images) > 4 else 1
  ncols = 4

  fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 6))

  for i, ax in enumerate(axes.flat):
    if i < len(images):
      ax.imshow(images[i])
      ax.set_xticks([])
      ax.set_yticks([])
    else:
      ax.axis("off")  # Turn off empty subplots

  plt.tight_layout()
  plt.show()


def save_images(images, folder):
  """Saves images to the specified folder.

  Args:
    images: A list of Image objects.
    folder: The folder to save the images to.
  """

  if not os.path.exists(folder):
    os.makedirs(folder)

  for idx, img in enumerate(images):
    img_path = os.path.join(folder, f"image_{idx}.png")
    img.save(img_path)
    print(f"Saved {img_path}")

def get_description(file_name):

  # Initialise a client
  storage_client = storage.Client()
  # Create a bucket object for our bucket
  bucket = storage_client.get_bucket(BUCKET)
  # Create a blob object from the filepath
  blob = bucket.blob(FOLDER+CSV_FILE_NAME)
  # Download the file to a destination
  blob.download_to_filename("output.csv")
  with open('output.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      if row[0] == file_name:
        print("From CSV: "+row[2])
        return row[2]

def get_image_promt(prompt_with_marketing,creativity):
  marketing_description = prompt_with_marketing.replace('\n', ' ').replace('\r', '')
  response = generation_model.predict(prompt=marketing_description,temperature=creativity,max_output_tokens=1020)
  print (">>>"+ response.text.replace('\n', ' ').replace('\r', ''))
  return response.text.replace('\n', ' ').replace('\r', '')

def download_image_from_cloud_storage(bucket_name, file_name, local_path):
    """Downloads a file from Cloud Storage to a local path.

    Args:
        bucket_name (str): The name of the Cloud Storage bucket.
        file_name (str): The name of the file to download.
        local_path (str): The local path to save the file to.
    """

    # Construct a client side representation of a Cloud Storage bucket.
    storage_client = storage.Client()

    # Construct a client side representation of a Cloud Storage file.
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download the file from Cloud Storage to a local path.
    blob.download_to_filename(local_path)

    #return blob.download_as_bytes()


def list_files(directory):
  """List all files in a directory."""
  for entry in os.listdir(directory):
    full_path = os.path.join(directory, entry)
    if os.path.isfile(full_path):
      print(full_path)

def upload_image_to_cloud_storage(bucket_name, file_name, file_path):
  # Upload the image file to Cloud Storage.
  #print(f"Uploading {file_name} to gs://{bucket_name}/{file_path}{file_name} in Cloud Storage.")
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(file_name)
  blob.upload_from_filename(file_name)
  #print(f"File {file_name} uploaded to {bucket_name}.")

def make_blob_public(bucket_name, blob_name):
    """Makes a blob publicly accessible."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.make_public()

    print(
        f"Blob {blob.name} is publicly accessible at {blob.public_url}"
    )

PROJECT_ID = os.environ["PROJECT_ID"]
vertexai.init(project=PROJECT_ID, location="us-central1")
generation_model = TextGenerationModel.from_pretrained("text-unicorn")
LOCATION = "us-central1"  # @param {type:"string"}
IMAGE_MODEL_NAME = "imagegeneration@002"  # @param {type:"string"}
BUCKET = ""  # @param {type:"string"}
FOLDER = ""  # @param {type:"string"}
CSV_FILE_NAME = ""  # @param {type:"string"}
PREDICTION_ENDPOINT = (
    f"https://{LOCATION}-aiplatform.googleapis.com/v1/"
    f"projects/{PROJECT_ID}/locations/{LOCATION}/"
    f"publishers/google/models/{IMAGE_MODEL_NAME}:predict"
)
os.environ["PREDICTION_ENDPOINT"] = PREDICTION_ENDPOINT
for file in os.listdir('.'):
  if file.endswith('.png'):
    os.remove(file)
  if file.endswith('.jpeg'):
    os.remove(file)
  if file.endswith('.csv'):
    os.remove(file)


# images = []
# DESCRIPTION = "" # @param {type:"string"}
# CREATIVITY = 1 # @param {type:"slider", min:0, max:1, step:0.1}
# NUM_IMAGES_PER_ATTEMPT = 1 # @param {type:"slider", min:1, max:6, step:1}
# PROMPT = "Generate a very descriptive prompt for a background image given a description. \nHere is an example: \nDESCRIPTION: A futuristic light beer for cyberpunk videogames lovers. \nPROMPT: A blurred image of a city with multiple neon lights and colorful lights. It is night and we can see robots in the background carrying boxes and metal artifacts."
# PROMPT = PROMPT + "\nDESCRIPTION: " + DESCRIPTION + " \nPROMPT: "
#PROMPT = "Write a prompt for an image generator model for a background image given the following description" # @param {type:"string"}