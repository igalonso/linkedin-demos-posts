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
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig
from datetime import datetime
import google.auth

# Imports the google.auth.transport.requests transport
from google.auth.transport import requests
MODEL="gemini-1.0-pro-001"

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

        model = GenerativeModel("gemini-1.0-pro-001")
        generation_config = GenerationConfig(
            temperature=0,
            top_p=1.0,
            top_k=32,
            candidate_count=1,
            max_output_tokens=8192,
        )
        prompt = "Make a summary in bullet points of the following conditions: "+ str(response)
        # summary = model.predict(
        #     "Make a summary in bullet points of the following conditions: "+ str(response),
        #     **parameters,
        # )
        summary = model.generate_content(prompt, stream=False,generation_config=generation_config)
        return summary.candidates[0].content.parts[0].text
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

        model = GenerativeModel(MODEL)
        # summary = model.predict(
        #     "Make a summary in bullet points of the following procedures: "+ str(response),
        #     **parameters,
        # )
        # model = GenerativeModel("gemini-1.0-pro-001")
        generation_config = GenerationConfig(
            temperature=0,
            top_p=1.0,
            top_k=32,
            candidate_count=1,
            max_output_tokens=8192,
        )
        prompt = "Make a summary in bullet points of the following procedures: "+ str(response)
        # summary = model.predict(
        #     "Make a summary in bullet points of the following conditions: "+ str(response),
        #     **parameters,
        # )
        summary = model.generate_content(prompt, stream=False,generation_config=generation_config)
        return summary.candidates[0].content.parts[0].text
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

        model = GenerativeModel(MODEL)
        generation_config = GenerationConfig(
            temperature=0,
            top_p=1.0,
            top_k=32,
            candidate_count=1,
            max_output_tokens=8192,
        )
        prompt = "Make a summary in bullet points of the following patient profile: "+ str(response)
        summary = model.generate_content(prompt, stream=False,generation_config=generation_config)
        return summary.candidates[0].content.parts[0].text


        # summary = model.predict(
        #      "Make a summary in bullet points of the following patient profile: "+ str(response),
        #     **parameters,
        # )
        # return summary.candidates[0]
    else:
        return None

def get_triage_level(symptoms: str,patient_id: str, max_er_capacity: int, current_er_patients: int):
    print("current er patients", current_er_patients)
    print("max er capacity", max_er_capacity)
    profile = get_patient_profile(patient_id)
    history = get_patient_conditions(patient_id)
    procedures = get_patient_procedures(patient_id)
    json_format = {
        "symptoms": "symtoms of the patient",
        "patient_id": "id of the patient",
        "max_er_capacity": "maximum capacity of the ER room",
        "current_er_patients": "number of current patients in the ER room",
        "triage_level": "selected triage. Eiter Low, Medium or High",
        "reasoning": "reasoning for triage",
        "patient_history": "patient's history"
    }
    prompt = f"You are a ER triage agent that helps nurses triage patients that come to the hospital. You need to take into account the symptoms of the patient, the current capacity of the ER and the history of the patient.\nThe patient {patient_id} has the following profile: {profile}. \nThe patient has the following symptoms: {symptoms}. \nThe patient has the following history: {history}. \nThe patient has the following procedures: {procedures}. \nThe maximum capacity of the ER room is {max_er_capacity}. \nThe number of current patients in the ER room is {current_er_patients}. \nDetermine the triage level for the patient usong the current json_format: {json_format} \nDo not use single quotes for this JSON. Use double quotes."
    model = GenerativeModel(MODEL)
    generation_config = GenerationConfig(
        temperature=0,
        top_p=1.0,
        top_k=32,
        candidate_count=1,
        max_output_tokens=8192,
    )
    # prompt = "Make a summary in bullet points of the following patient profile: "+ str(response)
    summary = model.generate_content(prompt, stream=False,generation_config=generation_config)
    print(summary.candidates[0].content.parts[0].text)
    return summary.candidates[0].content.parts[0].text

    