# CareerPilot AI – Multi-Agent Career Mentor System

CareerPilot AI is a production-ready multi-agent system designed to act as an automated career coach. It parses user resumes, detects skill gaps, recommends projects, builds learning roadmaps, generates interview preparation material, and outputs a publication-ready career guidance report.

## Folder Structure

```
CareerPilot-AI/
│
├── agents/         # Multi-Agent orchestrations & Task configurations (CrewAI)
├── pages/          # Streamlit dashboard pages for multi-page UI
├── utils/          # Utility modules (PDF parser, PDF generator, Groq API client, Vector DB)
├── data/           # Persistent data storage (ChromaDB vectors, raw files)
├── reports/        # Staging folder for generated PDF career reports
├── assets/         # CSS styles, images, icons, and diagrams
├── config/         # System settings and prompts
│
├── app.py          # Main Streamlit web application entrypoint
├── requirements.txt# Core project dependencies
├── .env            # Private configuration environment variables (Ignored by Git)
├── .env.example    # Configuration template
└── README.md       # Project documentation and setup guide
```

---

## Phase 1 Setup Instructions

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Environment Setup
Clone the repository, then navigate to the project directory:
```bash
# In your terminal
cd CareerPilot
```

Create a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (Windows Command Prompt)
.\venv\Scripts\activate.bat

# Activate virtual environment (macOS / Linux)
source venv/bin/activate
```

### 3. Install Dependencies
Install all package requirements defined for the project foundation:
```bash
pip install -r requirements.txt
```

### 4. API Keys and Credentials
Copy the environment variables template and configure your Groq API Key:
```bash
cp .env.example .env
```
Open the `.env` file and replace `your_groq_api_key_here` with a valid API key from [Groq Console](https://console.groq.com/).

---

## Testing Instructions

To run the Streamlit starter application and test the Groq API connectivity:

```bash
streamlit run app.py
```

1. Open your browser to the local server URL printed by Streamlit (typically `http://localhost:8501`).
2. Verify that **API Configuration Status** shows as **Ready** in both the sidebar and the main panel.
3. Scroll to the **Groq Connection Validator** section.
4. Keep the default test prompt or write a custom prompt (e.g. "What is CrewAI?").
5. Click the **Test Connection** button.
6. Confirm that the validation returns a success message and prints the LLM's response.
