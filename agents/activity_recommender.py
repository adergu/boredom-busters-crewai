from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

def get_activity_recommender_agent():
    return Agent(
        role="Activity Recommender",
        goal="Suggest 3-5 customized activities that match the user's mood and constraints.",
        backstory=(
            "You are a creative AI with expertise in curating fun and engaging activities. "
            "You recommend tailored experiences based on mood and constraints."
        ),
        llm=ChatGroq(
            api_key=GROQ_API_KEY,
            model_name="groq/llama3-70b-8192",
            temperature=0.7,
            max_tokens=600
        ),
        verbose=True,
        allow_delegation=False
    )