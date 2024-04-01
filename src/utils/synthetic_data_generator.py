#!/usr/bin/env python

import json
import argparse
import pandas as pd

import vertexai
from vertexai.generative_models import GenerativeModel, Part

from google.cloud import bigquery
from google.cloud.bigquery.enums import WriteDisposition
from google.cloud.exceptions import NotFound


PROMPT = """generate 10 rows of second hand products for sale in Spanish cities with the following fields and structure:
    [
        {"product": "product name specifying the brand",
        "description": "description of the second hand object with deatils",
        "category": "category of the object one of these: Cars, Motorcycles, Motorcycles and Accessories, Fashion and Accessories, Real Estate, Technology and Electronics, Movies and Telephony, Informatics, Sports and Hobbies, Bicycles, Consoles and Video Games, Home and Garden, Household Appliances, Cinemas, Books and Music, Children and Babies, Construction and Reforms, Industry and Agriculture, Employment, Services, Others",
        "brand": "brand",
        "model": "model",
        "year": "year as an integer. Avoid using N/A, if year is unknown use 0",
        "condition": "condition from one of these: new, slightly used, used, heavy used, refurbished, for parts, not working",
        "color": "color",
        "reason_for_selling": "reason for selling",
        "price": "price quantity as a float. It is very important that you DO NOT use commas in the price field to avoid parsing errors",
        "negotiable": "yes/no",
        "delivery": "yes/no",
        "location": "location",
        "contact": "contact"},
    ]
    DO NOT add any " in the fields to avoid errors when parsing the generated json.
    Do NOT use "null" as a value. Leave the String empty "" instead.
    Generate the output in Spanish"""


def create_bigquery_table(dataset_id, table_id):
    client = bigquery.Client()

    dataset = client.get_dataset(dataset_id)  

    schema = [
        bigquery.SchemaField("product", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("description", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("category", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("brand", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("model", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("year", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("condition", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("color", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("reason_for_selling", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("price", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("negotiable", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("delivery", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("location", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("contact", "STRING", mode="REQUIRED"),
    ]

    try:
        client.get_table(bigquery.Table(dataset.table(table_id)))
        print("Table already exists.")
    except NotFound:
        table = bigquery.Table(dataset.table(table_id), schema=schema)
        table = client.create_table(table) 
        print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id, exists_ok=True))
        
def insert_into_bigquery(bq_dataset, bq_table, data):
    
    client = bigquery.Client()
    table = client.get_table("{}.{}".format(bq_dataset, bq_table))
    
    df = pd.DataFrame(data)
    job_config = bigquery.LoadJobConfig(write_disposition=WriteDisposition.WRITE_APPEND)
    job = client.load_table_from_dataframe(df, table, job_config=job_config)  # Make an API request.
    job.result()  # Waits for the job to complete.


def main(n_rows_in_tens, bq_dataset, bq_table):
    config = {
        "max_output_tokens": 8192,
        "temperature": 0.9,
        "top_p": 1
    }
    
    model = GenerativeModel("gemini-1.0-pro-001")
    
    for i in range(n_rows_in_tens):
        response = model.generate_content(PROMPT, generation_config=config)
        print(response.text)

        try:
            json_data = json.loads(response.text)
            insert_into_bigquery(bq_dataset, bq_table, json_data)
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates synthetic data')
    parser.add_argument('--bq-dataset', type=str, required=True, help='BigQuery dataset to write to')
    parser.add_argument('--bq-table', type=str, required=True, help='BigQuery table to write to')
    parser.add_argument('--n-rows-in-tens', type=int, required=True, help='Number of rows in tens to generate')
    args = parser.parse_args()
    create_bigquery_table(args.bq_dataset, args.bq_table)
    main(args.n_rows_in_tens, args.bq_dataset, args.bq_table)

