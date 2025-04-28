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

def get_mood_analyzer_agent():
    return Agent(
        role="Mood Analyzer",
        goal="Analyze the user's emotional state based on their responses to questions.",
        backstory=(
            "You are an empathetic AI skilled at understanding human emotions. "
            "You analyze responses to determine the user's mood and map it to a predefined category."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )