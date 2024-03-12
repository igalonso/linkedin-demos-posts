import base64
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig

import numpy as np
import json
from PIL import Image
import io

from google.cloud import speech_v1p1beta1 as speech
import io

def transcribe_audio_file(audio_file, model):
    client = speech.SpeechClient()

    # with io.open(file_path, "rb") as audio_file:
    #     content = audio_file.read()
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        audio_channel_count=2,
        enable_separate_recognition_per_channel=True,
        model=model,
    )

    response = client.recognize(config=config, audio=audio)

    # for result in response.results:
    #     print("Transcript: {}".format(result.alternatives[0].transcript))
    return response.results
# Call the function with the path to your audio file
def calling_gemini_magic(transcript):
    json_format = {
        "sentiment": "One of these values: positive, negative, neutral",
        "sentiment_reason": "A reason for that sentiment",
        "summary_of_conversation": "A summary of the conversation",
        "category": "One or more of these values: sales, support, billing, other",
        "next_action": "one or more of these values: follow_up, no_follow_up, escalate, no_escalate, other, upsell, cross_sell, no_upsell, no_cross_sell, other",
    }
    prompt = f"Give me information of this conversation in the following format {json_format} using double quotes in the JSON\n CONVERSATION: {transcript}"
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0,
        "top_k": 40
    }
    generation_config = GenerationConfig(
        temperature=0,
        top_p=1.0,
        top_k=32,
        candidate_count=1,
        max_output_tokens=8192,
    )
    model = GenerativeModel("gemini-pro")
    responses = model.generate_content(prompt, stream=False,generation_config=generation_config)
    
    # model = TextGenerationModel.from_pretrained("gemini-pro")
    # response = model.predict(
    #     prompt,
    #     **parameters
    # )
    # return response.text
    # print(responses)
    return json.loads(responses.candidates[0].content.parts[0].text.replace("'", '"'))

# response = transcribe_audio_file("commercial_stereo.wav", "telephony")
# # for alternative in response:
# #     if alternative.channel_tag == 1:
# #             print(alternative.alternatives[0].transcript)
# # print(response)
# print(calling_gemini_magic(response))