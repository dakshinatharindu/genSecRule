import os
from dotenv import load_dotenv
import openai

# Load .env into environment
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("NAVIGATOR_TOOLKIT_API_KEY"),
    base_url="https://api.ai.it.ufl.edu"
)

response = client.chat.completions.create(
    model="llama-3.1-8b-instruct",
    messages=[
        {
            "role": "user",
            "content": "this is a test request, write a short poem"
        }
    ]
)

print(response.choices[0].message.content)
