from vertexai.preview.generative_models import GenerativeModel, GenerationResponse, GenerationConfig
import json
import os
from google.cloud import texttospeech
import subprocess
import base64
import requests
from PIL import Image
from io import BytesIO
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
    headers = {
    "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }

    data = {
    "instances": [
        {
        "prompt": prompt,
        }
    ],
    "parameters": {
        "sampleCount": 1
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
  project_id = os.environ["PROJECT_ID"]
  model_id = os.environ["IMAGE_MODEL_NAME"]
  endpoint = (
        f"https://us-central1-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/us-central1/"
        f"publishers/google/models/{model_id}:predict"
    )
  response = requests.post(endpoint, headers=headers, data=data)

  if response.status_code != 200:
    print(response.request)
    # raise requests.exceptions.HTTPError(
    #     f"Error: {response.status_code} ({response.reason}) [{response.request.body}]")

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
  
def generate_summary(paragraph):
    # json_format = {
    #    "characters": "list of the name of the characters"
    #   #  "adventure": "a brief description of the adventure without naming the characters",
    # }
    prompt = f"Write a summary of the following paragraph: {paragraph}"
    generation_config = GenerationConfig(
        temperature=0.5,
        top_p=1.0,
        top_k=32,
        candidate_count=1,
        max_output_tokens=8192,
    )
    model = GenerativeModel("gemini-pro")
    responses = model.generate_content(prompt, stream=False, generation_config=generation_config)
    summary = responses.candidates[0].content.parts[0].text
    return summary

def generate_kid_images(paragraph, context):
    prompt = f"An image for a book for young people that represents the following paragraph in a colorful yet simple style: {paragraph} \n Use also the following context {context}"
    images = generate_images(prompt, number_of_images=1, image_size=512)
    return images
def generate_story(kid_name, kid_age, kid_interests):
    prompt = f"You are a storyteller for kids. Write me a story that casts {kid_name}, a {kid_age} year old kid who likes {kid_interests}. Make it entretaining and easy to read and don't refer to the kid's age nor refer to the kid as a kid. Make the kid feel like and adult. The story should be at least 100 words long."
    generation_config = GenerationConfig(
        temperature=0.5,
        top_p=1.0,
        top_k=32,
        candidate_count=1,
        max_output_tokens=8192,
    )
    model = GenerativeModel("gemini-pro")
    responses = model.generate_content(prompt, stream=False, generation_config=generation_config)
    story = responses.candidates[0].content.parts[0].text
    return story

def narrate_story(story, output_filename):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=story)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-F",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

# story = generate_story("Mario", 8, "robots")
# paragraphs = story.split("\n")
# for paragraph in paragraphs:
#     print(paragraph)
# generate_kid_images("In a bustling town, there lived an imaginative 8-year-old boy named Mario who adored robots. His eyes sparkled with wonder whenever he saw a robotic toy or a TV show featuring mighty machines.")