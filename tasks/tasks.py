from crewai import Task
from agents.mood_analyzer import get_mood_analyzer_agent
from agents.info_collector import get_info_collector_agent
from agents.activity_recommender import get_activity_recommender_agent
import json

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

