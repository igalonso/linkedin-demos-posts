from dotenv import load_dotenv
import numpy as np

import os
import base64
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageOps as PIL_ImageOps
from PIL.ExifTags import TAGS, GPSTAGS
import json
import subprocess
import requests
from google.cloud import storage
import io
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, GenerationResponse, GenerationConfig
from typing import List

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

from langchain_community.retrievers import GoogleVertexAISearchRetriever
from langchain_community.llms import VertexAI
from langchain.chains import RetrievalQA
import json

temp = 0.8

load_dotenv()
if __name__ == "__main__":
    pass

project_id = os.getenv("PROJECT_ID")
location = os.getenv("LOCATION")
data_store_id = os.getenv("DATA_STORE_ID")


def string_meter_to_number(string):
    return float(string.split(" ")[0])


def upload_video_to_gcs_return_url(video_path, bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(video_path)
    return f"gs://{bucket_name}/{blob_name}"

def get_golf_query(query: str):
    #print(query)
    retriever = GoogleVertexAISearchRetriever(
        project_id=os.environ["PROJECT_ID"],
        location_id=os.environ["LOCATION_ID"],
        data_store_id=os.environ["DATA_STORE_ID"],
        max_documents=3,
        max_extractive_answer_count=3,
        get_extractive_answers=True,
    )
    llm = VertexAI(temperature=0, verbose=True,model_name="text-bison@001")
    retrieval_qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
    )
    result = retrieval_qa({"query": query})
    print(result["result"])
    return result["result"]

def get_book_context():
    # response = search_sample(
    response = {
        "initial_swing": get_golf_query('perfect initial swing position. give it in bullet points'),
        "swing_movement": get_golf_query('perfect swing movement. give it in bullet points'),
        "finishing_swing": get_golf_query('perfect finishing for the swing. give it in bullet points')
    }
    return json.dumps(response)




def get_swing_video_inputs(video_local_path, distance, club):


    video_path = upload_video_to_gcs_return_url(video_local_path, "igngar-golf-buddy-videos", "video.mp4")
    json_format = {
        "tips": [{
            "tip": "the name of the tip",
            "explanation": "detailed explanation of the tip",
            "why":"why are you giving me this tip? what did you see in the video that trigger this tip",
            "emoji": "the best emoji to be displayed with the tip",
            "confidence": "the confidence of the tip. It should be a number between 0 and 5. 1 means you are totally sure of the tip and 0 means you are not sure at all."
        }],
        "positives": [{
            "feedback": "the name of the positive feedback",
            "confidence": "the confidence of the feedback. It should be a number between 0 and 5. 1 means you are totally sure of the feedback and 0 means you are not sure at all."
        }]
        }
    context = json.loads(get_book_context())
    context_initial = context["initial_swing"]
    context_movement = context["swing_movement"]
    context_finishing = context["finishing_swing"]
    prompt = f"Given the following video with this club: {club} presented bellow and the distance of {distance} in the shot I just made give me \n - 3 tips to improve my swing like a pro and 3 positive feedbacks.\n The response should be in the following json format using double quotes in your response:\n {json_format}\nUse the following golf tips for swings: Initial position {context_initial}\n Swing movement {context_movement}\nSwing finishing: {context_finishing}\n RESPONSE:"
    
    multimodal_model = GenerativeModel("gemini-1.0-pro-vision-001")
    responses = multimodal_model.generate_content([prompt, generative_models.Part.from_uri(video_path,mime_type="video/mp4")],stream=False)
    response = responses.candidates[0].content.parts[0].text.replace('```json', '').replace('```', '')
    print(response)
    return json.loads(response.replace("'", "\""))

# def get_swing_video_positive_inputs(video, statistics, distance, club):
#     video_path = upload_video_to_gcs_return_url(video, "igngar-golf-buddy-videos", "video.mp4")
#     json_format = [{"feedback": "the name of the positive feedback",
#         "explanation": "detailed explanation of the positive feedback",
#         "why":"why are you giving me this feedback? what did you see in the video that trigger this feedback",
#         "emoji": "the best emoji to be displayed with the feedback",
#         "confidence": "the confidence of the feedback. It should be a number between 0 and 5. 1 means you are totally sure of the feedback and 0 means you are not sure at all."}]

#     prompt = f"Given the following video, the average statistics of my shots with this club and the distance of the shot I just made ({distance}), give me 3 positive things I did right. The response should be in the following json format using double quotes:\n {json_format}\n STATISTICS:\n {statistics}\n RESPONSE:"
#     multimodal_model = GenerativeModel("gemini-pro-vision")
#     generation_config = GenerationConfig(
#         temperature=temp,
#         top_p=1.0,
#         top_k=32,
#         candidate_count=1,
#         max_output_tokens=8192,
#     )
#     responses = multimodal_model.generate_content([prompt, generative_models.Part.from_uri(video_path,mime_type="video/mp4")],stream=False)
#     #responses = multimodal_model.generate_content(["What is in the video? ",generative_models.Part.from_uri("gs://cloud-samples-data/video/animals.mp4", mime_type="video/mp4"),

#     response = responses.candidates[0].content.parts[0].text.replace('```json', '').replace('```', '')
#     return json.loads(response)

def collect_statistic_data(club):
    with open('assets/toptracer-scrapping/statistics_toptracer.json', 'r') as f:
        data = json.load(f)
    data_curated = []
    for shot in data:
        if shot["club"] is not None and shot["club"] == club.upper():
            
            data_curated.append(shot)
    response = {
        "average_distance": np.mean([float(shot["total_distance"].split(" ")[0]) for shot in data_curated]),
        "average_curve" :  np.mean([float(shot["curve"].split("m")[0]) for shot in data_curated]),
        "average_height" :  np.mean([float(shot["height"].split("m")[0]) for shot in data_curated]),
        "hang_time" :  np.mean([float(shot["hang_time"].split("s")[0].strip().replace(",",".")) for shot in data_curated]),
        "average_speed" :  np.mean([float(shot["speed"].split(" km/h")[0]) for shot in data_curated]),
        "average_flat_carry" :  np.mean([float(shot["flat_carry"].split("m")[0]) for shot in data_curated]),
        "average_launch_angle" :  np.mean([float(shot["launch_angle"].split(" ")[0]) for shot in data_curated]),
        "average_landing_angle" :  np.mean([float(shot["landing_angle"].split(" ")[0]) for shot in data_curated]),
    }
    return response




def button_started(video, club, distance):
    statistics = collect_statistic_data(club)
    swing = get_swing_video_inputs("temp/front_swing.mp4",distance,club)
    # positive =get_swing_video_positive_inputs("temp/front_swing.mp4", statistics,distance,club)
    # posture = get_swing_posture_inputs(posture, statistics,distance,club)
    # grip = get_hand_grip_video_inputs(hand_grip, statistics,distance,club)

    return swing

# statistics = collect_statistic_data("Driver", 125)
# print(statistics)