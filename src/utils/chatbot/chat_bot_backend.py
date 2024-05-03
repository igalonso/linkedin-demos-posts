from flask import Flask, request, jsonify
from vertexai.generative_models import GenerativeModel

# TODO: Import and set up the Gemini LLM model

app = Flask(__name__)

def text_summarization(
    text: str):
    """Summarization Example with a Large Language Model"""
    prompt = f"You are an assistant that summarizes requests to be sent by email. The text to be summarized is: \n {text} \n SUMMARY:"
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0,
        "top_k": 40,
        "stream": False
    }
    model = GenerativeModel("gemini-1.0-pro")
    response = model.generate_content(
        prompt,stream=False
    )
    return {"response": response.text}


@app.route('/demo', methods=['POST'])
def summarize():
    # Extract the text from the request data
    print(request.json)
    text = request.json['request']

    # TODO: Use the Gemini LLM model to generate a summary
    summary = text_summarization(text) 
    return jsonify(summary), 200

if __name__ == '__main__':
    app.run(debug=True)