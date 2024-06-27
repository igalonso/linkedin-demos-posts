from vertexai.generative_models import GenerativeModel
from vertexai.preview import reasoning_engines
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core import prompts
from typing import List
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")



load_dotenv()
if __name__ == "__main__":
    pass


def search_jira(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
) -> List[discoveryengine.SearchResponse]:
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.SearchServiceClient(client_options=client_options)

    # The full resource name of the search app serving config
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=2,
    )

    response = client.search(request)
    print(response)

    return response

def open_new_ticket_jira(query:str,issuetype:str):
    """
    Open a new Jira ticket based on the query to be troubleshooted by a human agent.

    Args:
        query (str): The query to open a new Jira ticket.
        issuetype (str): The type of issue to be created. Types are: "Bug", "Report an incident", "Get IT help", "Problem".
    
    Returns:
        str: The Jira ticket number.
    """
     # Configuration - replace these with your actual details
    jira_url = os.environ.get("JIRA_URL")
    api_token = JIRA_API_TOKEN
    user_email = os.environ.get("JIRA_USER_EMAIL")
    project_key = os.environ.get("JIRA_PROJECT_KEY")
    
    # The URL for creating an issue
    url = f"{jira_url}/rest/api/2/issue"
    
    # The headers for authentication and content type
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # The payload for the new issue
    payload = json.dumps({
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": f"New issue from IT support helper: {query}",
            "description": f"Automatically created ticket based on user query: {query}",
            "issuetype": {
                "name": issuetype
            }
        }
    })
    
    # Make the request
    response = requests.post(url, headers=headers, data=payload, auth=HTTPBasicAuth(user_email, api_token))
    
    # Check for successful creation
    if response.status_code == 201:
        issue_key = response.json().get("key")
        print(f"Ticket {issue_key} created successfully.")
        return issue_key
    else:
        print(f"Failed to create ticket: {response.content}")
        return None

    


def retrieve_jira_tickets(query: str):
    """
    Retrieve Jira tickets based on the query to gather past occurences of a problem and what the solution was. Use this tool to find solutions to problems.

    Args:
        query (str): The query to search for Jira tickets.

    Returns:
        list: The complete Jira lust tickets with resolution information.
    """
    project_id = os.environ.get("PROJECT_ID")
    location = "global"         # Values: "global", "us", "eu"
    engine_id = os.environ.get("JIRA_ENGINE_ID")
    return search_jira(project_id, location, engine_id, query)

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
    "temperature": 0,
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

store = {}

def get_session_history(session_id: str):
    print("get_session_history")
    print(session_id)
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def agent_invoke(prompt: str, uuid: str):
    agent = reasoning_engines.LangchainAgent(
        model=model_agent,
        tools=[retrieve_jira_tickets],
        model_kwargs=model_kwargs,
        agent_executor_kwargs={"return_intermediate_steps": True},
        chat_history=get_session_history
    )
    
    response = agent.query(
        input=prompt,
        config={"configurable":{"session_id":uuid}}
    )
    return response