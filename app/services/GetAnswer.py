from app.services.GeminiService import generate_from_prompt  # Your Gemini wrapper
from app.services.buildPrompt import build_prompt

def process_api_results(api_response):
    responses = []
    for item in api_response["results"]:
        query = item["query"]
        chunks = item["chunks"]  # list of strings
        prompt = build_prompt(query, chunks)
        answer = generate_from_prompt(prompt)
        responses.append(answer)
    return responses

