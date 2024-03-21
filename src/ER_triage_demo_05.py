import os
from dotenv import load_dotenv
from langchain.llms import VertexAI
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.agents import AgentType
from langchain.llms import VertexAI
import os
import json
from dotenv import load_dotenv
import vertexai 
from vertexai.language_models import TextGenerationModel
from datetime import datetime
import google.auth

# Imports the google.auth.transport.requests transport
from google.auth.transport import requests


load_dotenv()
if __name__ == "__main__":
    pass


def get_patient_conditions(patient_id):
    # Get credentials
    credentials, project = google.auth.default()
    # scoped_credentials = credentials.with_scopes(
    #     ["https://www.googleapis.com/auth/cloud-platform"]
    # )
    session = requests.AuthorizedSession(credentials)
    base_url = "https://healthcare.googleapis.com/v1"
    # The name of the dataset
    dataset_name = '{}/projects/{project_id}/locations/{location}/datasets/{dataset_id}'.format(
        base_url,
        project_id=os.environ["FHIR_PROJECT_ID"],
        location=os.environ["FHIR_REGION"],
        dataset_id=os.environ["FHIR_DATASET_ID"]  # replace with your dataset id
    )

    # The name of the FHIR store
    fhir_store_name = '{}/fhirStores/{}'.format(dataset_name, os.environ["FHIR_DATASTORE_ID"])  # replace with your FHIR store id

    # The FHIR resource
    fhir_resource_name = '{}/fhir/Condition?subject=Patient/{}'.format(fhir_store_name, patient_id)

    # Make an authenticated API request
    headers = {'Content-Type': 'application/fhir+json;charset=utf-8'}
    response = session.get(fhir_resource_name, headers=headers)

    if response.status_code == 200:
        project_id = os.environ["PROJECT_ID"]
        location = "europe-west1"
        vertexai.init(project=project_id, location=location)
        parameters = {
            "temperature": 0,  # Temperature controls the degree of randomness in token selection.
            "max_output_tokens": 2040,  # Token limit determines the maximum amount of text output.
            "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
            "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
        }

        model = TextGenerationModel.from_pretrained("text-bison@002")
        summary = model.predict(
            "Make a summary in bullet points of the following conditions: "+ str(response),
            **parameters,
        )
        return summary.candidates[0]
    else:
        return None
def get_patient_procedures(patient_id):
    # Get credentials
    credentials, project = google.auth.default()
    # scoped_credentials = credentials.with_scopes(
    #     ["https://www.googleapis.com/auth/cloud-platform"]
    # )
    session = requests.AuthorizedSession(credentials)
    base_url = "https://healthcare.googleapis.com/v1"
    # The name of the dataset
    dataset_name = '{}/projects/{project_id}/locations/{location}/datasets/{dataset_id}'.format(
        base_url,
        project_id=os.environ["FHIR_PROJECT_ID"],
        location=os.environ["FHIR_REGION"],
        dataset_id=os.environ["FHIR_DATASET_ID"]  # replace with your dataset id
    )

    # The name of the FHIR store
    fhir_store_name = '{}/fhirStores/{}'.format(dataset_name, os.environ["FHIR_DATASTORE_ID"])  # replace with your FHIR store id

    # The FHIR resource
    fhir_resource_name = '{}/fhir/Procedure?subject=Patient/{}'.format(fhir_store_name, patient_id)

    # Make an authenticated API request
    headers = {'Content-Type': 'application/fhir+json;charset=utf-8'}
    response = session.get(fhir_resource_name, headers=headers)

    if response.status_code == 200:
        project_id = os.environ["PROJECT_ID"]
        location = "europe-west1"
        vertexai.init(project=project_id, location=location)
        parameters = {
            "temperature": 0,  # Temperature controls the degree of randomness in token selection.
            "max_output_tokens": 2040,  # Token limit determines the maximum amount of text output.
            "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
            "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
        }

        model = TextGenerationModel.from_pretrained("text-bison@002")
        summary = model.predict(
            "Make a summary in bullet points of the following procedures: "+ str(response),
            **parameters,
        )
        return summary.candidates[0]
    else:
        return None
def get_patient_profile(patient_id):
    # Get credentials
    credentials, project = google.auth.default()
    # scoped_credentials = credentials.with_scopes(
    #     ["https://www.googleapis.com/auth/cloud-platform"]
    # )
    session = requests.AuthorizedSession(credentials)
    base_url = "https://healthcare.googleapis.com/v1"
    # The name of the dataset
    dataset_name = '{}/projects/{project_id}/locations/{location}/datasets/{dataset_id}'.format(
        base_url,
        project_id=os.environ["FHIR_PROJECT_ID"],
        location=os.environ["FHIR_REGION"],
        dataset_id=os.environ["FHIR_DATASET_ID"]  # replace with your dataset id
    )

    # The name of the FHIR store
    fhir_store_name = '{}/fhirStores/{}'.format(dataset_name, os.environ["FHIR_DATASTORE_ID"])  # replace with your FHIR store id

    # The FHIR resource
    fhir_resource_name = '{}/fhir/Patient?subject=Patient/{}'.format(fhir_store_name, patient_id)

    # Make an authenticated API request
    headers = {'Content-Type': 'application/fhir+json;charset=utf-8'}
    response = session.get(fhir_resource_name, headers=headers)

    if response.status_code == 200:
        project_id = os.environ["PROJECT_ID"]
        location = "europe-west1"
        vertexai.init(project=project_id, location=location)
        parameters = {
            "temperature": 0,  # Temperature controls the degree of randomness in token selection.
            "max_output_tokens": 2040,  # Token limit determines the maximum amount of text output.
            "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
            "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
        }

        model = TextGenerationModel.from_pretrained("text-bison@002")
        summary = model.predict(
             "Make a summary in bullet points of the following patient profile: "+ str(response),
            **parameters,
        )
        return summary.candidates[0]
    else:
        return None

def determine_triage_level(query):
    project_id = os.environ["PROJECT_ID"]
    location = "europe-west1"
    vertexai.init(project=project_id, location=location)
    parameters = {
        "temperature": 0,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 2040,  # Token limit determines the maximum amount of text output.
        "top_p": 0,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        query,
        **parameters,
    )
    return response.text
    
patient_history = Tool(
    name="patient_history",
    func=get_patient_conditions,
    description="Get patient history from FHIR using the patient's ID",
)
patients_triage = Tool(
    name="patients_triage",
    func=determine_triage_level,
    description="useful for triage patients in the ER room based on the current patients in the ER room, the maximum capacity of the ER room, the symptoms of the patient, the patient's history and the patient's profile",
)
patient_profile = Tool(
    name="patient_profile",
    func=get_patient_profile,
    description="Get patient profile from FHIR using the patient's ID",
)

def get_er_agent(temp):
    print("*" * 79)
    print("AGENT: ER agent!")
    print("*" * 79)
    llm = VertexAI(temperature=temp, verbose=True, max_output_tokens=8192,model_name=os.environ["MODEL_NAME"])
    tools_for_agent = [patient_history, patients_triage,patient_profile]
    agent = initialize_agent(
        tools_for_agent,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent


def triage_patient(symtoms: str , patients_id: str, max_er_capacity: int, current_er_patients: int):
    json_format = {
        "symptoms": "symtoms of the patient",
        "patient_id": "id of the patient",
        "max_er_capacity": "maximum capacity of the ER room",
        "current_er_patients": "number of current patients in the ER room",
        "triage_level": "selected triage",
        "reasoning": "reasoning for triage",
        "patient_history": "patient's history"
    }
    task = "You are a ER triage agent that helps nurses triage patients that come to the hospital. You need to find the patients history with the followint ID: "+ patients_id+ ". You need to find the profile of the patient to know it's age with the following Patient ID: "+ patients_id+ ". The levels of Triage are Low, Medium, High in priority. Take into account the current patients in the ER room to perform your triage." + symtoms+ ". The current patients in the ER room are: "+ str(current_er_patients)+ " and the maximum capacity of the ER room is: "+ str(max_er_capacity)+"\n The formant should be as follows: " + str(json_format) + "\n Do not use single quotes for this JSON. Use double quotes."
    agent = get_er_agent(0)
    results = agent.run(task)
    print(results)
    # response = results
    # print(response)
    return results.replace("'", "\"")
    # return results
    