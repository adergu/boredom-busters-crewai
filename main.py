import json
import os
import logging
from dotenv import load_dotenv
from crewai import Crew
from agents import get_mood_analyzer_agent, get_mood_analyzer_task, get_info_collector_agent, get_info_collector_task, get_activity_recommender_agent, get_activity_recommender_task
from tenacity import retry, stop_after_attempt, wait_fixed
from warnings import filterwarnings

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Suppress warnings
filterwarnings("ignore")

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

def load_json(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {e}")
        return {}

def save_json(file_path, data):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")

def get_user_input(prompt, type_cast=str, validator=None):
    while True:
        try:
            value = type_cast(input(prompt).strip())
            if validator and not validator(value):
                raise ValueError("Invalid input")
            return value
        except ValueError as e:
            print(f"Error: {e}")
            logger.error(f"Invalid user input: {e}")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def analyze_mood(crew, responses):
    logger.info("Analyzing mood with responses: %s", responses)
    task = get_mood_analyzer_task(responses)
    crew.tasks = [task]
    result = crew.kickoff()
    try:
        content = result.raw.strip()
        logger.info("Mood analyzer raw output: %s", content)
        if content.startswith("```json") and content.endswith("```"):
            content = content[7:-3].strip()
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON from mood analyzer: %s", e)
        raise ValueError(f"Invalid JSON response: {e}")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def collect_constraints(crew, constraints):
    logger.info("Collecting constraints: %s", constraints)
    task = get_info_collector_task(constraints)
    crew.tasks = [task]
    result = crew.kickoff()
    try:
        content = result.raw.strip()
        logger.info("Info collector raw output: %s", content)
        if content.startswith("```json") and content.endswith("```"):
            content = content[7:-3].strip()
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON from info collector: %s", e)
        raise ValueError(f"Invalid JSON response: {e}")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def recommend_activities(crew, prefs, activities):
    logger.info("Recommending activities for preferences: %s", prefs)
    task = get_activity_recommender_task(prefs, activities)
    crew.tasks = [task]
    result = crew.kickoff()
    try:
        content = result.raw.strip()
        logger.info("Activity recommender raw output: %s", content)
        if content.startswith("```json") and content.endswith("```"):
            content = content[7:-3].strip()
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON from activity recommender: %s", e)
        raise ValueError(f"Invalid JSON response: {e}")

def calculate_metrics(suggestions, user_prefs, rating):
    logger.info("Calculating metrics for rating: %s", rating)
    uf = rating / 5.0  # User Feedback
    rs = 0.0
    if suggestions:
        relevance_scores = []
        for s in suggestions:
            score = 0.0
            if s["duration"] <= user_prefs["time"]:
                score += 1.0
            if s["cost"] <= user_prefs["budget"]:
                score += 1.0
            if s["people"] == user_prefs["people"]:
                score += 1.0
            if s.get("mood", "").lower() == user_prefs["mood"].lower():
                score += 1.0
            relevance_scores.append(score / 4.0)
        rs = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0
    w1, w2 = 0.6, 0.4  # Adjusted weights
    aes = w1 * uf + w2 * rs
    if aes >= 1.8:
        result = "Excellent"
    elif aes >= 1.5:
        result = "Good"
    elif aes >= 1.0:
        result = "Just OK"
    else:
        result = "Bad"
    logger.info("Metrics: UF=%.2f, RS=%.2f, AES=%.2f, Result=%s", uf, rs, aes, result)
    return uf, rs, aes, result

def save_preferences(crew):
    user_id = get_user_input("Enter user ID (e.g., user1): ", str, lambda x: x.strip() != "")
    try:
        # Collect mood responses
        questions = [
            "How you doin' today? (e.g., feeling great, kinda tired): ",
            "How was your day so far? (e.g., awesome, stressful): "
        ]
        responses = [get_user_input(q) for q in questions]
        mood_data = analyze_mood(crew, responses)
        
        # Collect constraints
        constraints = {
            "budget": get_user_input(
                "What's your budget? (e.g., 20, or 0 for none): ",
                float,
                lambda x: 0 <= x <= 1000
            ),
            "time": get_user_input(
                "How much time do you have? (minutes, e.g., 60): ",
                int,
                lambda x: 1 <= x <= 300
            ),
            "people": get_user_input(
                "How many people? (e.g., 1 for solo, 2 for couple): ",
                int,
                lambda x: 1 <= x <= 10
            )
        }
        constraints_data = collect_constraints(crew, constraints)
        
        if not mood_data.get("mood") or "errors" in constraints_data:
            print("Failed to collect valid preferences.")
            if "errors" in constraints_data:
                print("Errors:", ", ".join(constraints_data["errors"]))
            return
        
        prefs = {
            "mood": mood_data["mood"],
            "time": constraints_data["time"],
            "budget": constraints_data["budget"],
            "people": constraints_data["people"],
            "history": []
        }
        user_data = load_json("data/user_preferences.json")
        user_data[user_id] = prefs
        save_json("data/user_preferences.json", user_data)
        print(f"Mood interpreted as: {prefs['mood']}")
        print("Preferences saved successfully.")
    except Exception as e:
        print(f"Error: {e}")
        logger.error("Error in save_preferences: %s", e)

def get_suggestions(crew):
    user_id = get_user_input("Enter user ID (e.g., user1): ", str, lambda x: x.strip() != "")
    user_data = load_json("data/user_preferences.json")
    if user_id not in user_data:
        print("User ID not found. Please save preferences first.")
        return
    
    try:
        prefs = user_data[user_id]
        activities = load_json("data/activities.json")
        suggestions = recommend_activities(crew, prefs, activities)
        
        if not suggestions or len(suggestions) < 3:
            print("Insufficient suggestions received. Try again later.")
            return
        
        print("\nActivity Suggestions:")
        for i, s in enumerate(suggestions, 1):
            print(f"{i}. {s['name']} ({s['duration']} min, ${s['cost']}, {s['people']} people)")
            print(f"   {s['description']}")
        
        rating = get_user_input(
            "Rate these suggestions (1-5): ",
            int,
            lambda x: 1 <= x <= 5
        )
        
        uf, rs, aes, result = calculate_metrics(suggestions, prefs, rating)
        print("\nPerformance Metrics:")
        print(f"User Feedback (UF): {uf:.2f}")
        print(f"Relevance Score (RS): {rs:.2f}")
        print(f"Activity Effectiveness Score (AES): {aes:.2f}")
        print(f"Result: {result}")
        
        # Store feedback in history
        user_data[user_id]["history"].append({
            "suggestions": suggestions,
            "rating": rating,
            "uf": uf,
            "rs": rs,
            "aes": aes,
            "result": result
        })
        save_json("data/user_preferences.json", user_data)
        print("Feedback saved.")
    except Exception as e:
        print(f"Error: {e}")
        logger.error("Error in get_suggestions: %s", e)

def main():
    print("=== Boredom Busters ===")
    try:
        # Initialize CrewAI with agents
        crew = Crew(
            agents=[
                get_mood_analyzer_agent(),
                get_info_collector_agent(),
                get_activity_recommender_agent()
            ],
            tasks=[],
            verbose=True
        )
        logger.info("Crew initialized with agents: %s", [agent.role for agent in crew.agents])
        
        while True:
            print("\n1. Save Preferences\n2. Get Activity Suggestions\n3. Exit")
            choice = get_user_input("Choose an option: ", str, lambda x: x in ["1", "2", "3"])
            if choice == "1":
                save_preferences(crew)
            elif choice == "2":
                get_suggestions(crew)
            elif choice == "3":
                print("Goodbye!")
                break
    except Exception as e:
        print(f"Unexpected error: {e}")
        logger.error("Unexpected error in main: %s", e)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logger.error("Unexpected error: %s", e)