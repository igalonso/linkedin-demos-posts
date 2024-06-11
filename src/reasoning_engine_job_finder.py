from vertexai.preview import reasoning_engines
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.memory import ChatMessageHistory
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core import prompts
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
import json
import requests


load_dotenv()
if __name__ == "__main__":
    pass

LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT=os.environ["LANGCHAIN_ENDPOINT"]
LANGCHAIN_API_KEY= os.environ["LANGCHAIN_API_KEY"]
from langsmith import traceable



model = "gemini-1.5-pro-001"
embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@latest")
offer_loader = CSVLoader(file_path="src/utils/jobs_csv.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
    })
offers_data = offer_loader.load()
offers_db = Chroma.from_documents(offers_data, embeddings)
offers_retriever = offers_db.as_retriever(search_kwargs={"k": 3})

safety_settings = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}
ip_address = "88.1.213.70"
model_kwargs = {
    "temperature": 0.3,
    "max_output_tokens": 1000,
    "top_p": 0.95,
    "top_k": 40,
    "safety_settings": safety_settings,
}

def get_scrape_linkedin_profile(linkedin_profile_url: str):
    """
    Retrieves the information of a LinkedIn profile given the LinkedIn URL. Information includes the headline, summary, experiences, education, occupation, country and city of residence.

    Args:
        linkedin_profile_url: The URL of the LinkedIn profile to scrape.
    
    Returns: 
        dict: A dictionary containing the information of the LinkedIn profile.
            Example: {"headline": "Software Engineer at Google", "summary": "I'm a software engineer with 5 years of experience...",
                "experiences": [["Google", "Software Engineer", "2018-01-01", "2023-01-01"], ["Facebook", "Software Engineer", "2015-01-01", "2018-01-01"]],
                "education": [["Stanford University", "Bachelor's Degree in Computer Science", "2011-01-01", "2015-01-01"]], "occupation": "Software Engineer", "country": "United States", "city": "San Francisco"}
    """
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"

    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    response = requests.get(
        api_endpoint,
        params={"url": linkedin_profile_url, "extra": "include"},
        headers=header_dic,
    )
    data = response.json()
    with open("assets/linkedin_profile.json", "r") as f:
        data = json.load(f)
    experiences = data["experiences"]
    headline = data["headline"]
    summary = data["summary"]
    occupation = data["occupation"]
    country = data["country_full_name"]
    city = data["city"]
    experiences = []
    for experience in data["experiences"]:
        experiences.append([experience["company"], experience["title"], experience["starts_at"], experience["ends_at"]])
    educations = []
    for education in data["education"]:
        educations.append([education["school"], education["degree_name"], education["starts_at"], education["ends_at"]])
    final_response = {"headline": headline, "summary": summary, "experiences": experiences, "education": education, "occupation": occupation, "country": country, "city": city}
    return final_response


def search_job_offers(query:str):
    """Retrieves the best job offer in the database given the query of the user

    Args:
        query: The job that the user is seeking

    Returns:
        dict: A dictionary containing the information of the most similar jobs.
            Example: [Document(page_content='job_id: 10\njob_description: Customer Service Representative
            job_location: Phoenix, AZ\njob_benefits: Health insurance, 401k, paid time off
            job_salary: 60,000 USD', metadata={'row': 9, 'source': 'src/utils/jobs_csv.csv'}), Document(page_content='job_id: 7
            job_description: Sales Engineer\njob_location: Los Angeles, CA\njob_benefits: Health insurance, 401k, paid time off
            job_salary: 100,000 USD', metadata={'row': 6, 'source': 'src/utils/jobs_csv.csv'}), Document(page_content='job_id: 4
            job_description: Marketing Manager\njob_location: Chicago, IL\njob_benefits: Health insurance, 401k, paid time off
            job_salary: 110,000 USD', metadata={'row': 3, 'source': 'src/utils/jobs_csv.csv'})]
            offer_link: https://dsfsdg.com', metadata={'row': 3, 'source': 'src/utils/jobs_csv.csv'})]
    """
    return offers_retriever.invoke(query)
def get_location():
    """
    Retrieves the location information of the user.
    Returns:
        tuple: A tuple containing the city, region, and country of the IP address.
            Example: ("Mountain View", "California", "United States")

    """
    
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}')
        response.raise_for_status()
        data = response.json()
        return data['city'], data['regionName'], data['country']
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def get_exchange_rate(currency_from: str = "USD", currency_to: str = "EUR"):
    """Retrieves the exchange rate between two currencies on a specified date.

    Uses the Frankfurter API (https://api.frankfurter.app/) to obtain
    exchange rate data.

    Args:
        currency_from: The base currency (3-letter currency code).
            Defaults to "USD" (US Dollar).
        currency_to: The target currency (3-letter currency code).
            Defaults to "EUR" (Euro).

    Returns:
        dict: A dictionary containing the exchange rate information.
            Example: {"amount": 1.0, "base": "USD", "date": "2023-11-24",
                "rates": {"EUR": 0.95534}}
    """
    import requests
    response = requests.get(
        f"https://api.frankfurter.app/latest",
        params={"from": currency_from, "to": currency_to},
    )
    return response.json()

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

# Initialize session history
store = {}



def get_session_history(session_id: str):
    print(session_id)
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


@traceable
def agent_invoke(prompt, uuid: str):
    agent = reasoning_engines.LangchainAgent(
        model=model,
        tools=[get_exchange_rate,search_job_offers,get_scrape_linkedin_profile,get_location],
        model_kwargs=model_kwargs,
        agent_executor_kwargs={"return_intermediate_steps": True},
        chat_history=get_session_history
    )
    
    response = agent.query(
        input=prompt,
        config={"configurable":{"session_id":uuid}}
    )
    return response

