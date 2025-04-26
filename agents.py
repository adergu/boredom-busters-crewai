from crewai import Agent, Task
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="groq/llama3-70b-8192",  # Explicitly set provider prefix
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

def get_mood_analyzer_task(responses):
    return Task(
        description=(
            f"Analyze the user's mood based on their responses: {json.dumps(responses)}. "
            "Map to one of: happy, tired, adventurous, relaxed, social. "
            "Return a JSON object wrapped in ```json\n...\n```, e.g., ```json\n{\"mood\": \"tired\"}\n```. "
            "Ensure output is valid JSON with no extra text."
        ),
        expected_output="A JSON object with a single key 'mood' and a valid mood label",
        agent=get_mood_analyzer_agent()
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

def get_info_collector_task(constraints):
    return Task(
        description=(
            f"Validate user constraints: {json.dumps(constraints)}. "
            "Ensure budget (0-1000), time (1-300 minutes), people (1-10). "
            "Return a JSON object wrapped in ```json\n...\n```, e.g., ```json\n{\"budget\": 5.0, \"time\": 60, \"people\": 1}\n```. "
            "Include an 'errors' list if validation fails, e.g., ```json\n{\"errors\": [\"Invalid budget\"]}\n```. "
            "Ensure output is valid JSON with no extra text."
        ),
        expected_output="A JSON object with validated constraints or an errors list",
        agent=get_info_collector_agent()
    )

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
            model_name="groq/llama3-70b-8192",  # Explicitly set provider prefix
            temperature=0.7,
            max_tokens=600
        ),
        verbose=True,
        allow_delegation=False
    )

def get_activity_recommender_task(prefs, activities):
    return Task(
        description=(
            f"User preferences: mood={prefs['mood']}, time={prefs['time']} minutes, "
            f"budget=${prefs['budget']}, people={prefs['people']}. "
            f"Available activities: {json.dumps(activities, indent=2)}. "
            "Suggest 3-5 activities that match the preferences. "
            "Each activity must include name, duration (minutes), cost ($), people, mood, and description. "
            "Return a JSON list wrapped in ```json\n...\n```, e.g., "
            "```json\n[{\"name\": \"Activity\", \"duration\": 30, \"cost\": 0, \"people\": 1, \"mood\": \"tired\", \"description\": \"Description\"}]\n```. "
            "Ensure output is valid JSON with no extra text."
        ),
        expected_output="A JSON list of 3-5 activities with required fields",
        agent=get_activity_recommender_agent()
    )