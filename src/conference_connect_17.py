import json
from google.cloud import bigquery
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
client = bigquery.Client()


def get_vector_search(text):
    options = '{"fraction_lists_to_search": 0.01}'
    client = bigquery.Client()
    query = f"""
        SELECT query.query, base.Name AS Name, base.Surname AS Surname, base.Email AS Email, base.Company AS Company, base.JobTitle AS JobTitle, base.Interests AS Interests
            FROM VECTOR_SEARCH(
            TABLE `conference_connect.attendees`, 'Embeddings',
            (
            SELECT ml_generate_embedding_result, content AS query
            FROM ML.GENERATE_EMBEDDING(
            MODEL `conference_connect.embedding_connection_model`,
            (SELECT "{text}" AS content))
            ),
            top_k => 3, options => '{options}')
    """
    print(query)
    query_job = client.query(query)
    results = query_job.result()
    candidates = []
    print("Results:")
    for row in results:
        print(f"{row.Name} {row.Surname}: {row.query}")
        json_result = {
            "Name": row.Name,
            "Surname": row.Surname,
            "Email": row.Email,
            "Company": row.Company,
            "JobTitle": row.JobTitle,
            "Interests": row.Interests
        }
        candidates.append(json_result)
    return candidates

