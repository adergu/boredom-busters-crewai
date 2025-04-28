import json
import random
import os
from crewai import Crew
from tasks.tasks import get_mood_analyzer_task, get_info_collector_task, get_activity_recommender_task
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
USER_PREFS_FILE = "data/user_preferences.json"
ACTIVITIES_FILE = "data/activities.json"

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: {file_path} contains invalid JSON.")
        return {}

def save_json_file(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {str(e)}")
        return False

def get_user_input(prompt, type_cast=float, valid_range=None):
    while True:
        try:
            value = type_cast(input(prompt))
            if valid_range and (value < valid_range[0] or value > valid_range[1]):
                print(f"Error: Value must be between {valid_range[0]} and {valid_range[1]}.")
                continue
            return value
        except ValueError:
            print("Error: Invalid input.")

def save_preferences():
    user_id = input("Enter user ID (e.g., user1): ")
    mood_response1 = input("How you doin' today? (e.g., feeling great, kinda tired): ")
    mood_response2 = input("How was your day so far? (e.g., awesome, stressful): ")
    budget = get_user_input("What's your budget? (e.g., 20, or 0 for none): ", float, (0, 1000))
    time = get_user_input("How much time do you have? (minutes, e.g., 60): ", int, (1, 300))
    people = get_user_input("How many people? (e.g., 1 for solo, 2 for couple): ", int, (1, 10))

    try:
        # Initialize Crew for mood analysis
        crew = Crew(
            agents=[],
            tasks=[get_mood_analyzer_task([mood_response1, mood_response2])],
            verbose=True
        )
        result = crew.kickoff()

        # Parse mood result (expecting JSON wrapped in ```json\n...\n```)
        mood_output = result.raw
        if mood_output.startswith("```json\n") and mood_output.endswith("\n```"):
            mood_json = json.loads(mood_output[8:-4])
            mood = mood_json.get("mood")
            if mood not in ["happy", "tired", "adventurous", "relaxed", "social"]:
                print("Error: Invalid mood returned.")
                return
        else:
            print("Error: Invalid mood analysis output format.")
            return

        print(f"Mood interpreted as: {mood}")

        # Validate constraints
        constraints = {"budget": budget, "time": time, "people": people}
        crew = Crew(
            agents=[],
            tasks=[get_info_collector_task(constraints)],
            verbose=True
        )
        constraint_result = crew.kickoff()

        constraint_output = constraint_result.raw
        if constraint_output.startswith("```json\n") and constraint_output.endswith("\n```"):
            constraint_json = json.loads(constraint_output[8:-4])
            if "errors" in constraint_json:
                print(f"Error: {constraint_json['errors']}")
                return
        else:
            print("Error: Invalid constraint validation output format.")
            return

        # Save preferences
        user_prefs = load_json_file(USER_PREFS_FILE)
        user_prefs[user_id] = {
            "mood": mood,
            "time": time,
            "budget": budget,
            "people": people,
            "history": user_prefs.get(user_id, {}).get("history", [])
        }
        if save_json_file(USER_PREFS_FILE, user_prefs):
            print("Preferences saved successfully.")
        else:
            print("Error: Failed to save preferences.")
    except Exception as e:
        print(f"Error in save_preferences: {str(e)}")

def get_suggestions():
    user_id = input("Enter user ID (e.g., user1): ")
    user_prefs = load_json_file(USER_PREFS_FILE)
    activities = load_json_file(ACTIVITIES_FILE)

    if user_id not in user_prefs:
        print("User ID not found. Please save preferences first.")
        return

    prefs = user_prefs[user_id]
    try:
        # Initialize Crew for activity recommendation
        crew = Crew(
            agents=[],
            tasks=[get_activity_recommender_task(prefs, activities)],
            verbose=True
        )
        result = crew.kickoff()

        # Parse recommendations
        suggestions_output = result.raw
        if suggestions_output.startswith("```json\n") and suggestions_output.endswith("\n```"):
            suggestions = json.loads(suggestions_output[8:-4])
        else:
            print("Error: Invalid suggestions output format.")
            return

        print("Activity Suggestions:")
        for i, activity in enumerate(suggestions, 1):
            print(f"{i}. {activity['name']} ({activity['duration']} min, ${activity['cost']}, {activity['people']} people)")
            print(f"   {activity['description']}")

        # Get user rating
        rating = get_user_input("Rate these suggestions (1-5): ", int, (1, 5))

        # Calculate performance metrics
        uf = rating / 5.0  # User Feedback
        rs = sum(1 for s in suggestions if s["mood"] == prefs["mood"]) / len(suggestions)  # Relevance Score
        aes = sum(1 for s in suggestions if s["duration"] <= prefs["time"] and s["cost"] <= prefs["budget"] and s["people"] <= prefs["people"]) / len(suggestions)  # Activity Effectiveness Score
        result = "Good" if uf >= 0.8 and rs >= 0.8 and aes >= 0.8 else "Bad"

        print("Performance Metrics:")
        print(f"User Feedback (UF): {uf:.2f}")
        print(f"Relevance Score (RS): {rs:.2f}")
        print(f"Activity Effectiveness Score (AES): {aes:.2f}")
        print(f"Result: {result}")

        # Save feedback
        user_prefs[user_id]["history"].append({
            "suggestions": suggestions,
            "rating": rating,
            "uf": uf,
            "rs": rs,
            "aes": aes,
            "result": result
        })
        if save_json_file(USER_PREFS_FILE, user_prefs):
            print("Feedback saved.")
        else:
            print("Error: Failed to save feedback.")
    except Exception as e:
        print(f"Error in get_suggestions: {str(e)}")

def main():
    print("=== Boredom Busters ===")
    while True:
        print("\n1. Save Preferences")
        print("2. Get Activity Suggestions")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            save_preferences()
        elif choice == "2":
            get_suggestions()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()