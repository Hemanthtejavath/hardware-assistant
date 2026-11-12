import os

from dotenv import load_dotenv
from google import genai

from hardware_tools import (
    get_cpu_details,
    get_memory_details,
    get_storage_details,
    get_gpu_details
)

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found.")

# Connect to Gemini
client = genai.Client(api_key=api_key)


# Give Gemini access to approved hardware functions
tools = [
    get_cpu_details,
    get_memory_details,
    get_storage_details,
    get_gpu_details
]


# Ask Gemini a hardware question
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="How many physical and logical CPU cores does my laptop have?",
    config={
        "tools": tools
    }
)

print("\nGemini response:")
print(response.text)

client.close()
