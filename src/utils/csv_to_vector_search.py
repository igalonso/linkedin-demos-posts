from google.cloud import aiplatform
from google.cloud import storage
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_vertexai import (
    VectorSearchVectorStore,
    VectorSearchVectorStoreDatastore,
)
record_data = [
  {
    "id": "1",
    "job_description": "Software Engineer",
    "job_location": "San Francisco, CA",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "150,000 USD",
    "offer_link": "https://softeng.sanfrancisco.com/423213452345"
  },
  {
    "id": "2",
    "job_description": "Data Scientist",
    "job_location": "New York, NY",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "120,000 USD",
    "offer_link": "https://softeng.ny.com/423213452345"
  },
  {
    "id": "3",
    "job_description": "Product Manager",
    "job_location": "Seattle, WA",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "180,000 USD",
    "offer_link": "https://softeng.seat.com/4235462346"
  },
  {
    "id": "4",
    "job_description": "Marketing Manager",
    "job_location": "Chicago, IL",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "110,000 USD",
    "offer_link": "https://softeng.chicago.com/2436274235"
  },
  {
    "id": "5",
    "job_description": "Sales Manager",
    "job_location": "Boston, MA",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "130,000 USD",
    "offer_link": "https://softeng.boston.com/3456547456345"
  },
  {
    "id": "6",
    "job_description": "Project Manager",
    "job_location": "Austin, TX",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "140,000 USD",
    "offer_link": "https://softeng.austin.com/74658745674567"
  },
  {
    "id": "7",
    "job_description": "Sales Engineer",
    "job_location": "Los Angeles, CA",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "100,000 USD",
    "offer_link": "https://softeng.la.com/65437634573653"
  },
  {
    "id": "8",
    "job_description": "Web Developer",
    "job_location": "Denver, CO",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "120,000 USD",
    "offer_link": "https://softeng.denver.com/135445236436556"
  },
  {
    "id": "9",
    "job_description": "Accountant",
    "job_location": "Atlanta, GA",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "80,000 USD",
    "offer_link": "https://softeng.atlanta.com/2345234623452345"
  },
  {
    "id": "10",
    "job_description": "Customer Service Representative",
    "job_location": "Phoenix, AZ",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "60,000 USD",
    "offer_link": "https://softeng.phoeniz.com/356745463457546"
  },
  {
    "id": "11",
    "job_description": "Data Practicioner",
    "job_location": "New York, NY",
    "job_benefits": "Health insurance, 301k USD, office perks",
    "job_salary": "95,000 USD",
    "offer_link": "https://softeng.ny.com/3454464573456"
  },
  {
    "id": "12",
    "job_description": "Software Engineer",
    "job_location": "San Francisco, CA",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "150,000 USD",
    "offer_link": "https://softeng.sanfrancisco.com/423213452345"
  },
  {
    "id": "13",
    "job_description": "Data Scientist",
    "job_location": "New York, NY",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "120,000 USD",
    "offer_link": "https://softeng.ny.com/423213452345"
  },
  {
    "id": "14",
    "job_description": "Product Manager",
    "job_location": "Seattle, WA",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "180,000 USD",
    "offer_link": "https://softeng.seat.com/4235462346"
  },
  {
    "id": "15",
    "job_description": "Marketing Manager",
    "job_location": "Chicago, IL",
    "job_benefits": "Health insurance, 401k USD, paid time off",
    "job_salary": "110,000 USD",
    "offer_link": "https://softeng.chicago.com/2436274235"
  },
  {
    "id": "16",
    "job_description": "Teacher",
    "job_location": "London, UK",
    "job_benefits": "Pension, paid holidays, sick leave",
    "job_salary": "40,000 GBP",
    "offer_link": "https://teaching.london.com/1234567890"
  },
  {
    "id": "17",
    "job_description": "Nurse",
    "job_location": "Berlin, Germany",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "55,000 EUR",
    "offer_link": "https://nursing.berlin.com/9876543210"
  },
  {
    "id": "18",
    "job_description": "Chef",
    "job_location": "Paris, France",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "45,000 EUR",
    "offer_link": "https://chef.paris.com/1357924680"
  },
  {
    "id": "19",
    "job_description": "Sales Associate",
    "job_location": "Tokyo, Japan",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "35,000 JPY",
    "offer_link": "https://sales.tokyo.com/2468013579"
  },
  {
    "id": "20",
    "job_description": "Receptionist",
    "job_location": "Sydney, Australia",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "50,000 AUD",
    "offer_link": "https://reception.sydney.com/3579246801"
  },
  {
    "id": "21",
    "job_description": "Graphic Designer",
    "job_location": "Madrid, Spain",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "30,000 EUR",
    "offer_link": "https://design.madrid.com/4680135792"
  },
  {
    "id": "22",
    "job_description": "Social Media Manager",
    "job_location": "Rome, Italy",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "35,000 EUR",
    "offer_link": "https://socialmedia.rome.com/5792468013"
  },
  {
    "id": "23",
    "job_description": "Account Manager",
    "job_location": "Amsterdam, Netherlands",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "40,000 EUR",
    "offer_link": "https://account.amsterdam.com/6801357924"
  },
  {
    "id": "24",
    "job_description": "Project Coordinator",
    "job_location": "Dublin, Ireland",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "38,000 EUR",
    "offer_link": "https://project.dublin.com/7924680135"
  },
  {
    "id": "25",
    "job_description": "Customer Service Representative",
    "job_location": "Toronto, Canada",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "45,000 CAD",
    "offer_link": "https://customer.toronto.com/8013579246"
  },
  {
    "id": "26",
    "job_description": "Marketing Assistant",
    "job_location": "Melbourne, Australia",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "42,000 AUD",
    "offer_link": "https://marketing.melbourne.com/9135792468"
  },
  {
    "id": "27",
    "job_description": "Event Planner",
    "job_location": "New Delhi, India",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "50,000 INR",
    "offer_link": "https://event.delhi.com/0135792468"
  },
  {
    "id": "28",
    "job_description": "Translator",
    "job_location": "Seoul, South Korea",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "40,000 KRW",
    "offer_link": "https://translate.seoul.com/2357924680"
  },
  {
    "id": "29",
    "job_description": "Writer",
    "job_location": "Berlin, Germany",
    "job_benefits": "Health insurance, paid holidays, sick leave",
    "job_salary": "45,000 EUR",
    "offer_link": "https://writer.berlin.com/4680135792"
  },
  {
    "id": "30",
    "job_description": "Web Designer",
    "job_location": "London, UK",
    "job_benefits": "Pension, paid holidays, sick leave",
    "job_salary": "35,000 GBP",
    "offer_link": "https://webdesign.london.com/5792468013"
  }
]
project= "gen-ai-igngar"
location = "europe-southwest1"
gs_uri="gen-ai-indexes"
display_name="test_index"
DIMENSIONS = 768
UID = "fasdadgasdf"

# storage_client = storage.Client(project=project)

# bucket = storage_client.bucket(gs_uri)
# gcs_uri = f"gs://{gs_uri}"
# file_path = "src/utils/jobs_csv.csv"  # Replace with your file path
# blob_name = "jobs_csv.csv"  # Replace with your desired blob name
# blob = bucket.blob(blob_name)
# blob.upload_from_filename(file_path)
# print(f"File uploaded to {gcs_uri}/{blob_name}")
# Initialize the Vertex AI client
gcs_uri = f"gs://{gs_uri}"
aiplatform.init(project=project, location=location, staging_bucket=gcs_uri)
embedding_model = VertexAIEmbeddings(model_name="textembedding-gecko@003")

# # # Create Index
# # # my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
# # #     display_name = f"vs-quickstart-index-{UID}",
# # #     contents_delta_uri = gcs_uri,
# # #     dimensions = 5,
# # #     approximate_neighbors_count = 10,
# # # )
# # my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
# #     display_name=display_name,
# #     dimensions=DIMENSIONS,
# #     approximate_neighbors_count=150,
# #     distance_measure_type="DOT_PRODUCT_DISTANCE",
# #     index_update_method="STREAM_UPDATE",  # allowed values BATCH_UPDATE , STREAM_UPDATE
# # )
# # print(my_index.name)

# # ## create `IndexEndpoint`
# # my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
# #     display_name = f"vs-quickstart-index-endpoint-{UID}",
# #     public_endpoint_enabled = True
# # )

# # DEPLOYED_INDEX_ID = f"vs_quickstart_deployed_{UID}"

# # my_index_endpoint.deploy_index(
# #     index = my_index, deployed_index_id = DEPLOYED_INDEX_ID
# # )
my_index = "5135779230923096064"
my_index_endpoint = "7655261747460177920"
# texts = []
# metadatas = []
# for record in record_data:
#     # record = record.copy()
#     page_content = str(record)
#     record["page_content"] = page_content
#     texts.append(page_content)
#     if isinstance(page_content, str):
#         metadata = {**record}
#         metadatas.append(metadata)

gs_uri= "gen-ai-indexes-us-central1"

vector_store = VectorSearchVectorStore.from_components(
    project_id=project,
    region="us-central1",
    gcs_bucket_name=gs_uri,
    index_id=my_index,
    endpoint_id=my_index_endpoint,
    embedding=embedding_model,
)
# vector_store.add_texts(texts=texts, metadatas=metadatas, is_complete_overwrite=True)

print(vector_store.similarity_search("Programmer", k=1))