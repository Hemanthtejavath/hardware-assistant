
import streamlit as st
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

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Hardware Q&A Assistant",
    page_icon="💻",
    layout="centered"
)

st.title("💻 Hardware Q&A Assistant")
st.caption("Ask questions about your laptop hardware")

# Check API key
if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

# Create Gemini client
# Keep Gemini client alive across Streamlit reruns
@st.cache_resource
def get_gemini_client(api_key):
    return genai.Client(api_key=api_key)


client = get_gemini_client(api_key)

# Approved hardware tools
tools = [
    get_cpu_details,
    get_memory_details,
    get_storage_details,
    get_gpu_details
]

# Create chat session
if "chat" not in st.session_state:

    st.session_state.chat = client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction="""
            You are a Linux Hardware Q&A Assistant.
            Use the available hardware tools to collect information.
            Never invent hardware specifications.
            Explain results in simple English.
            If information is unavailable, say so.
            Only answer questions about computer hardware.
            """,
            tools=tools
        )
    )

# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask about your CPU, RAM, GPU or storage...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Checking your hardware..."):

            try:

                response = st.session_state.chat.send_message(question)

                answer = response.text or "I couldn't generate an answer."

            except Exception as error:

                answer = f"Sorry, something went wrong: {error}"

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
