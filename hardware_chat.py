
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from hardware_tools import (
    get_cpu_details,
    get_memory_details,
    get_storage_details,
    get_gpu_details
)


# Load Gemini API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found. Check your .env file.")


# Connect to Gemini
client = genai.Client(api_key=api_key)


# Approved hardware tools
tools = [
    get_cpu_details,
    get_memory_details,
    get_storage_details,
    get_gpu_details
]


# Instructions for Gemini

system_instruction = """
You are a Linux Hardware Q&A Assistant.

Your responsibility is to answer questions about computer hardware.

STRICT RULES:

1. Always use the available Python hardware tools
   when hardware information is required.

2. Never invent hardware specifications,
   measurements, or command outputs.

3. Only use information returned by the
   approved Python hardware functions.

4. Never execute arbitrary Linux commands.
   Never request shell commands from the user.

5. Perform read-only hardware inspection.
   Never modify system files, settings, or hardware.

6. If hardware information is unavailable,
   clearly explain that it could not be collected.

7. Explain technical information in simple English.

8. Remember previous conversation messages
   to understand follow-up questions.

9. If the question is unrelated to computer hardware,
   politely explain that you only answer hardware questions.

10. Distinguish WSL virtual hardware information
    from physical laptop hardware information.
"""



# Create a conversation with Gemini
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools
    )
)


def chatbot():

    print("========================================")
    print("       GEMINI HARDWARE Q&A ASSISTANT")
    print("========================================")
    print("Ask me anything about your laptop hardware.")
    print("Type 'exit' to quit.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit", "bye"]:

            print("Assistant: Goodbye!")
            break

        if not question:
            continue

        try:

            response = chat.send_message(question)

            print("\nAssistant:", response.text)

        except Exception as error:

            print("\nAssistant: Sorry, something went wrong.")
            print("Error:", error)


if __name__ == "__main__":

    try:
        chatbot()

    finally:
        client.close()
