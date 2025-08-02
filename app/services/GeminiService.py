from app.settings import settings
gemapi = settings.GeminiKey

from google import genai
from google.genai import types

client = genai.Client(api_key=gemapi)

def generate_from_prompt(prompt):

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="Please answer the query accoding to the context"),
    contents=prompt
    )
    return response.text