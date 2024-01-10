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
    

