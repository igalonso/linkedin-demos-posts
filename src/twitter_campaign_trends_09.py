from dotenv import load_dotenv
import tweepy
from textwrap import wrap
import numpy as np

import os
import base64
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageOps as PIL_ImageOps
from PIL.ExifTags import TAGS, GPSTAGS
import json
import subprocess
import requests
from io import BytesIO
from vertexai.preview.generative_models import GenerativeModel, GenerationResponse, GenerationConfig

load_dotenv()
if __name__ == "__main__":
    pass

temp = 0.8
NUM_IMAGES_PER_ATTEMPT = 1

def round_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def generate_photo(user_name,user_tag,text, hashtags, link,profile_pic,image_tweet): 
    # Constants
    # -----------------------------------------------------------------------------
    # Set the font to be used
    FONT_USER_INFO = ImageFont.truetype("assets/font.woff2", 90, encoding="utf-8")
    FONT_TEXT = ImageFont.truetype("assets/font.woff2", 110, encoding="utf-8")
    # Image dimensions (pixels)
    WIDTH = 2376
    HEIGHT = 4000
    # Color scheme
    COLOR_BG = 'white'
    COLOR_NAME = 'black'
    COLOR_TAG = (64, 64, 64)
    COLOR_TEXT = (15, 20, 25)
    COLOR_HASHTAG_LINK = (29, 155, 240)
  
    # Write coordinates
    COORD_PHOTO = (250, 170)
    COORD_NAME = (600, 185)
    COORD_TAG = (600, 305)
    COORD_TEXT = (250, 510)
    # Extra space to add in between lines of text
    LINE_MARGIN = 15
    # -----------------------------------------------------------------------------

    # Information for the image
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------

    # Setup of variables and calculations
    # -----------------------------------------------------------------------------
    # Break the text string into smaller strings, each having a maximum of 37\
    # characters (a.k.a. create the lines of text for the image)
    text_string_lines = wrap(text, 37)

    # Horizontal position at which to start drawing each line of the tweet body
    x = COORD_TEXT[0]

    # Current vertical position of drawing (starts as the first vertical drawing\
    # position of the tweet body)
    y = COORD_TEXT[1]

    # Create an Image object to be used as a means of extracting the height needed\
    # to draw each line of text
    temp_img = Image.new('RGB', (0, 0))
    temp_img_draw_interf = ImageDraw.Draw(temp_img)

    # List with the height (pixels) needed to draw each line of the tweet body
    # Loop through each line of text, and extract the height needed to draw it,\
    # using our font settings
    line_height = [
        temp_img_draw_interf.textsize(text_string_lines[i], font=FONT_TEXT)[1]
        for i in range(len(text_string_lines))
    ]
    # -----------------------------------------------------------------------------

    # Image creation
    # -----------------------------------------------------------------------------
    # Create what will be the final image
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(247,247,247))
    # Create the drawing interface
    draw_interf = ImageDraw.Draw(img)

    # Draw the user name
    draw_interf.text(COORD_NAME, user_name, font=FONT_USER_INFO, fill=COLOR_NAME)
    # Draw the user handle
    draw_interf.text(COORD_TAG, user_tag, font=FONT_USER_INFO, fill=COLOR_TAG)

    # Draw each line of the tweet body. To find the height at which the next\
    # line will be drawn, add the line height of the next line to the current\
    # y position, along with a small margin
    for index, line in enumerate(text_string_lines):
        # Draw a line of text
        draw_interf.text((x, y), line, font=FONT_TEXT, fill=COLOR_TEXT)
        # Increment y to draw the next line at the adequate height
        y += line_height[index] + LINE_MARGIN
    text_string_lines = wrap(hashtags, 20)
    for index, line in enumerate(text_string_lines):
        # Draw a line of text
        draw_interf.text((x, y), line, font=FONT_TEXT, fill=COLOR_HASHTAG_LINK)
        # Increment y to draw the next line at the adequate height
        y += line_height[index] + LINE_MARGIN
    draw_interf.text((x,y)," ", font=FONT_TEXT, fill=COLOR_TEXT)
    draw_interf.text((x,y)," ", font=FONT_TEXT, fill=COLOR_TEXT)
    draw_interf.text((x,y)," ", font=FONT_TEXT, fill=COLOR_TEXT)
    text_string_lines = wrap(link, 37)
    for index, line in enumerate(text_string_lines):
        # Draw a line of text
        draw_interf.text((x, y), line, font=FONT_TEXT, fill=COLOR_HASHTAG_LINK)
        # Increment y to draw the next line at the adequate height
        y += line_height[index] + LINE_MARGIN
    

    # Load the image_tweet following the text
    image_tweet = Image.open(image_tweet, 'r') 
    # Resize the image_tweet to be 1000 pixels wide, and keep the aspect ratio
    image_tweet.thumbnail((1500, 1500))
    # Paste the image_tweet into the working image
    image_tweet_rounded = round_corners(image_tweet, 100)
    y = y +40
    img.paste(image_tweet_rounded, (int(img.width // 2)-(int(image_tweet_rounded.width // 2)), y), mask=image_tweet_rounded)
    y = y + image_tweet_rounded.height + LINE_MARGIN
    image_banner = Image.open("assets/bottom_banner.png", 'r')
    # banner_height = image_banner.height
    # print(banner_height)
    # print(image_banner.width)

    # banner_width_multiplier = 2376 / image_banner.width
    # print(banner_height*banner_width_multiplier)
    # image_banner.thumbnail((2376, banner_height*banner_width_multiplier))
    img.paste(image_banner, (0, y), mask=image_banner)
    #img.paste(image_banner, (int(img.width // 2)-(int(image_banner.width // 2)), y))
    #img.paste(image_tweet_rounded, (int(img.width // 2)-(int(image_tweet_rounded.width // 2)), y))

    # Load the user photo (read-mode). It should be a 250x250 circle 
    user_photo = Image.open(profile_pic, 'r')

    # Paste the user photo into the working image. We also use the photo for\
    # its own mask to keep the photo's transparencies
    img.paste(user_photo, COORD_PHOTO, mask=user_photo)

    # Finally, save the created image
    #return img
    img.save('temp/output_tweet.png')

def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
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

def get_copy_from_trend(trend, product_name, product_desccription):
    # llm = VertexAI( model_name="text-bison-32k", temperature=temp, max_output_tokens=8100)
    json_format = {
        "body": "This is a tweet about the trend.",
        "hashtags": "hashtags to use in the tweet",
        "link": "the url of the offer",
        "features": "features of the product", 
        "call_to_action": "call to action",
        "additional_notes": "additional notes",
        "background_image": "background image description for the product in the tweet",
    }
    model = GenerativeModel("gemini-1.0-pro-001")

    prompt = f"Based on this product description and name, a trending topic from Twitter, give me an Ad copy to encourage our audience to buy it with an offer. Avoid using Logos or people nor hands. \n Product name: {product_name} \n Product description: {product_desccription}, \n Trending topic: {trend}. \n Use the following json format: {json_format} using double quotes."
    
    generation_config = GenerationConfig(
        temperature=temp,
        top_p=1.0,
        top_k=32,
        candidate_count=1,
        max_output_tokens=8192,
    )
    responses = model.generate_content(prompt, stream=False,generation_config=generation_config)
    return json.loads(responses.candidates[0].content.parts[0].text)

def generate_image_from_tweet(tweet, image):
    project_id = os.getenv('PROJECT_ID')
    location = os.getenv('LOCATION_TWITTER_PROJECT')
    image_model_name = os.getenv('IMAGE_MODEL_NAME')
    PREDICTION_ENDPOINT = (
        f"https://us-central1-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/us-central1/"
        f"publishers/google/models/{image_model_name}:predict"
    )
    os.environ["PREDICTION_ENDPOINT"] = PREDICTION_ENDPOINT
    in_file = open(image, "rb") # opening for [r]eading as [b]inary
    im = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
    prompt = f"Generate a background for an image given this tweet: {tweet}"
    images = generate_images(
        prompt=prompt,
        base_image=im,
        number_of_images=NUM_IMAGES_PER_ATTEMPT,
        is_product_image=True,
    )
    images[0].save("temp/output.png")


def gather_twitter_current_local_trends():
    return {
        "data": [
            {
                "trend_name": "Almería",
                "tweet_count": 232408
            },
            {
                "trend_name": "Oscars2024",
                "tweet_count": 2956
            },
            {
                "trend_name": "Negreira",
                "tweet_count": 2484
            },
            {
                "trend_name": "Bernabeu",
                "tweet_count": 11447
            },
            {
                "trend_name": "COAC2024P13",
                "tweet_count": 5565
            },
            {
                "trend_name": "FelizLunes",
                "tweet_count": 10077
            },
            {
                "trend_name": "Copacabana",
                "tweet_count": 35272
            },
            {
                "trend_name": "Ferreras",
                "tweet_count": 3662
            }
        ]
    }