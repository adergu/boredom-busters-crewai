from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="groq/llama3-70b-8192",
    temperature=0.5,
    max_tokens=300
)

def get_info_collector_agent():
    return Agent(
        role="Info Collector",
        goal="Gather and validate user's practical constraints such as budget, time, and number of people.",
        backstory=(
            "You are a meticulous AI designed to collect and validate user constraints. "
            "You ensure inputs are structured for downstream use."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )