import json
from google.cloud import bigquery
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
client = bigquery.Client()


from typing import List

from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


def embed_text(
    texts: List[str] = ["banana muffins? ", "banana bread? banana muffins?"],
    task: str = "RETRIEVAL_DOCUMENT",
    model_name: str = "textembedding-gecko@003",
) -> List[List[float]]:
    """Embeds texts with a pre-trained, foundational model."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    embeddings = model.get_embeddings(inputs)
    return [embedding.values for embedding in embeddings]

def insert_data():
    # Set the dataset_id to the ID of the dataset that contains your table.
    # Replace 'your_dataset' with your dataset ID.
    dataset_id = 'conference_connect'

    # Set the table_id to the ID of the table you want to create.
    # Replace 'your_table' with your table ID.
    table_id = 'attendees'

    # Set the path to your JSON file.
    # Replace 'path_to_json_file' with the path to your JSON file.
    json_filepath = 'conference_synth_data.json'
    # Load the JSON data
    with open('conference_synth_data.json', 'r') as f:
        data = json.load(f)

    # Connect to BigQuery
    create_table_query = f"""
        CREATE OR REPLACE TABLE `{dataset_id}.{table_id}` (
            Id INT64,
            Name STRING,
            Surname STRING,
            Email STRING,
            Company STRING,
            CompanyCategory STRING,
            JobTitle STRING,
            Customer BOOL,
            Prospect BOOL,
            GCPProjects STRING,
            Interests ARRAY<STRING>,
            Embeddings ARRAY<FLOAT64>
        );
    """

    client = bigquery.Client()
    purge_query = f"""
        -- I want to delete all rows from the attendees table
        DELETE
        FROM
            gen-ai-igngar.conference_connect.attendees
        WHERE TRUE;

        -- I want to delete all rows from the attendees table
        DELETE
        FROM
            gen-ai-igngar.conference_connect.interest
        WHERE TRUE
    """
    # query_job = client.query(create_table_query)
    # query_job.result()

    i=0
    j=0
    query = create_table_query
    query_job = client.query(query)
    query_job.result()
    for item in data:
        query = ""
        # if i > 1:
        #     break
        #embedding = create_embedding_from_item(item)
        # query = f"""
        #     INSERT INTO `{dataset_id}.{table_id}` (Name, Surname, Email, Company, CompanyCategory, Interests, JobTitle, Customer, Prospect, GCPProjects, Embedding)
        #     VALUES ('{item['Name']}', '{item['Surname']}', '{item['Email']}', '{item['Company Name']}', '{item['Category of the company']}', '{item['Interests']}', '{item['Job Title']}', '{item['Customer']}', '{item['Prospect']}', '{item['Recent Projects using Google Cloud']},'{embedding}')
        # """
        texts = []
        for interest in item['Interests']:
            texts.append(interest)
        texts.append(item['Recent Projects using Google Cloud'])
        texts.append(item['Job Title'])
        embedding = embed_text(texts,"SEMANTIC_SIMILARITY","textembedding-gecko@003")
        if item['Customer'] == 'yes':
            item['Customer'] = True
        else:
            item['Customer'] = False
        if item['Prospect'] == 'yes':
            item['Prospect'] = True
        else:    
            item['Prospect'] = False
        query = query +"\n" + f"""
            INSERT INTO `{dataset_id}.{table_id}` (Id, Name, Surname, Email, Company, CompanyCategory, JobTitle, Customer, Prospect, GCPProjects, Interests, Embeddings)
            VALUES ({i},'{item['Name']}', '{item['Surname']}', '{item['Email']}', '{item['Company Name']}', '{item['Category of the company']}', '{item['Job Title']}', {item['Customer']}, {item['Prospect']}, '{item['Recent Projects using Google Cloud']}', {item['Interests']},{embedding[0]});
        """
        # print(query)
        query_job = client.query(query)
        query_job.result()
        i+=1

def get_vector_search(text):
    options = '{"fraction_lists_to_search": 0.01}'
    client = bigquery.Client()
    query = f"""
        SELECT query.query, base.Name AS Name, base.Surname AS Surname, base.Email AS Email, base.Company AS Company, base.JobTitle AS JobTitle
            FROM VECTOR_SEARCH(
            TABLE `conference_connect.attendees`, 'Embeddings',
            (
            SELECT ml_generate_embedding_result, content AS query
            FROM ML.GENERATE_EMBEDDING(
            MODEL `conference_connect.embedding_connection_model`,
            (SELECT "{text}" AS content))
            ),
            top_k => 5, options => '{options}')
    """
    print(query)
    query_job = client.query(query)
    results = query_job.result()
    print("Results:")
    for row in results:
        print(f"{row.Name} {row.Surname}: {row.query}")
    return results

#insert_data()
get_vector_search("Containers")