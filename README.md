
# 💻 Gemini Hardware Q&A Assistant

link : https://hemanthtejavath-hardware-assistant-app-i6nm9x.streamlit.app/


An AI-powered hardware assistant that collects real system hardware information from a Linux environment and answers user questions in natural language using Google Gemini.

## Features

- CPU information: model, architecture, physical and logical cores.
- RAM information: total, used, free and available memory.
- GPU information: model, memory, temperature and utilization.
- Storage information: detected disks, capacity, model and device properties.
- Gemini function calling for hardware inspection.
- Natural-language answers and follow-up conversations.
- Streamlit chat interface.
- Read-only, allow-listed hardware inspection functions.
- Structured hardware data and error handling.

## Technology Stack

- Python
- Google Gemini API
- Google Gen AI SDK
- Streamlit
- Linux hardware inspection commands

## Project Structure

hardware-assistant/
│
├── app.py
├── hardware_info.py
├── hardware_tools.py
├── gemini_test.py
├── gemini_tools_test.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

## Installation

### 1. Clone the repository

git clone YOUR_REPOSITORY_URL

cd hardware-assistant

### 2. Create a virtual environment

python3 -m venv venv

### 3. Activate the environment

source venv/bin/activate

### 4. Install dependencies

pip install -r requirements.txt

### 5. Configure Gemini API key

Create a `.env` file in the project directory:

GEMINI_API_KEY=your_api_key_here

Never commit your API key to GitHub.

### 6. Run the application

streamlit run app.py

Open the local URL displayed in the terminal.

## Architecture

User Question
      |
      v
Streamlit Chat Interface
      |
      v
Google Gemini
      |
      v
Function Calling
      |
      v
Python Hardware Tools
      |
      v
Linux Inspection Commands
      |
      v
Structured Hardware Information
      |
      v
Gemini Natural-Language Response

## Safety and Limitations

- Only predefined hardware inspection functions are exposed to Gemini.
- No arbitrary user-generated shell commands are executed.
- Hardware inspection is read-only.
- Missing commands and unavailable information are handled.
- Hardware information is collected from the Linux environment.
- When running under WSL2, some devices may be virtualized.
- Hardware data is sent to Google's Gemini API for processing.

## Future Improvements

- Additional motherboard and memory-slot information.
- Better support for different Linux distributions.
- More comprehensive automated testing.
- Optional local LLM support.
- Improved hardware compatibility.

## Author

Hemanth
