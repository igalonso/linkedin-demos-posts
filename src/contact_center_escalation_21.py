import base64
from vertexai.generative_models import GenerativeModel, Part, Tool
import json
from vertexai.preview import reasoning_engines
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
# from langchain.memory import ChatMessageHistory
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core import prompts
import os
import requests
from langchain_community.agent_toolkits import GmailToolkit

model = GenerativeModel(model_name="gemini-1.5-flash-001")
model_agent = "gemini-1.5-pro-001"
safety_settings = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}
model_kwargs = {
    "temperature": 0.3,
    "max_output_tokens": 1000,
    "top_p": 0.95,
    "top_k": 40,
    "safety_settings": safety_settings,
}

# Define prompt template
prompt = {
    "history": lambda x: x["history"],
    "input": lambda x: x["input"],
    "agent_scratchpad": (
        lambda x: format_to_openai_function_messages(x["intermediate_steps"])
    ),
} | prompts.ChatPromptTemplate.from_messages(
    [
        ("placeholder", "{history}"),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
    

def transcribe_audio_file(audio_file):

    json_format = {"transcription": 
        [{"speaker": "1", "text": "Hello, how are you?"}, {"speaker": "2", "text": "I am fine, thank you"}]
    }
    prompt = f"Give me the transcription of this conversation in the following format {json_format}. Respond only with the JSON and using double quotes on it"
    audio_file = Part.from_data(base64.b64encode(audio_file).decode("utf-8"), mime_type="audio/mpeg")
    contents = [audio_file, prompt]  # Make sure both audio_file and prompt are in the list
    responses = model.generate_content(contents)
    response = responses.text
    return json.loads(response)

# Call the function with the path to your audio file
def get_call_meta_info(audio_file):
    json_format = {
        "sentiment": "One of these values: positive, negative, neutral",
        "sentiment_reason": "A reason for that sentiment",
        "summary_of_conversation": "A summary of the conversation",
        "category": "One or more of these values: sales, support, billing, other",
        "next_action": "one or more of these values: follow_up, no_follow_up, escalate, no_escalate, other, upsell, cross_sell, no_upsell, no_cross_sell, other",
    }
    prompt = f"Give me the following information of this conversation in the following format {json_format}. Respond only with the JSON and using double quotes on it"
    audio_file = Part.from_data(base64.b64encode(audio_file).decode("utf-8"), mime_type="audio/mpeg")
    contents = [audio_file, prompt]  # Make sure both audio_file and prompt are in the list
    responses = model.generate_content(contents)
    response = responses.text
    # print(response)
    return json.loads(response)

def send_email(email: str):
    """Sends an email in case that an escalation is needed.

    Args:
        email: The content of the email to send including situation, reason, category and summary of actions to perform.

    Returns:
        str: The email sent.
    """
    print(f"I've sent this email: \n {email} \n")
    return email

def agent_invoke(conclussions, email: str):
    prompt = f"You are a supervisor agent of a call center. Given the following conclussions act accordingly: {conclussions}. If the situation is dangerous, make a clear statement of the next action points. For escalation emails, send it to the following email: {email} and then respond with the email sent."
    agent = reasoning_engines.LangchainAgent(
        model=model_agent,
        tools=[send_email],
        model_kwargs=model_kwargs,
        agent_executor_kwargs={"return_intermediate_steps": True}
    )
    
    response = agent.query(
        input=prompt,
        config={"configurable":{"session_id":"fsdfsdgdsfsdf"}}
    )
    return response