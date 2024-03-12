from google.cloud import bigquery
from vertexai.preview.generative_models import GenerativeModel, GenerationResponse, GenerationConfig
import json

def retrieve_json_nominations():
    with open("assets/oscars2024.json", 'r') as f:
        data = json.load(f)
    return data


def recommend_movies(selected_categories, selected_movies):
    movies = retrieve_json_nominations()
    json_format = {
        "id": "id of the movie recommended",
        "movie_recommendation": "name of the movie recommendated",
        "recommendation_reason": "a reasoning for the recommendation",        
        "plot": "plot of the movie",
        "poster": "url to the poster of the movie"
    }
    prompt = f"Give me one recommendation from these movies {movies} based on the user selected categories: {selected_categories} and example of liked movies {selected_movies} in the following format {json_format} using double quotes in the JSON. Reference to one of the liked movies when giving the recommendation."
    generation_config = GenerationConfig(
        temperature=0.5,
        top_p=1.0,
        top_k=32,
        candidate_count=1,
        max_output_tokens=8192,
    )
    model = GenerativeModel("gemini-pro")
    
    responses = model.generate_content(prompt, stream=False,generation_config=generation_config)
    print(responses)
    return json.loads(responses.candidates[0].content.parts[0].text)
    

def load_categories():
    client = bigquery.Client()
    query = """
        SELECT DISTINCT category
        FROM `gen-ai-igngar.oscar_winners.refined`,
        UNNEST(Categories) AS category
    """
    query_job = client.query(query)
    results = query_job.result()
    categories = [row.category for row in results]
    return categories

def load_oscar_winners():
    client = bigquery.Client()
    query = """
        SELECT Film, Year
        FROM `gen-ai-igngar.oscar_winners.refined`
        WHERE winner = TRUE
        ORDER BY Year DESC;
    """
    query_job = client.query(query)
    results = query_job.result()
    winners = []
    for row in results:
        winners.append(f"{row.Year}, {row.Film}")  
    return winners
unique_categories = load_categories()
unique_movies = load_oscar_winners()

def return_unique_categories():
    return unique_categories
def return_unique_movies():
    return unique_movies


# categories = ['fantasy', 'horror', 'drama', 'comedy']
# movies = ['2021, Promising young woman', '2022, The Whale']
# print(recommend_movies(categories, movies))