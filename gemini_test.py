import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found. Check your .env file.")

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Send a test question
response = client.models.generate_content(
   model="gemini-3.5-flash-lite",
    contents="Explain what a CPU is in two simple sentences."
)

print("Gemini response:")
print(response.text)    

client.close()
