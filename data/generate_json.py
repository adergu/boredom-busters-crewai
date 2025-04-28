import json
import os
import random

def ensure_directory():
    os.makedirs("data", exist_ok=True)

def generate_user_preferences():
    moods = ["happy", "tired", "adventurous", "relaxed", "social"]
    users = {}
    for i in range(1, 51):  # Generate 50 users
        user_id = f"user{i}"
        users[user_id] = {
            "mood": random.choice(moods),
            "time": random.randint(30, 180),  # 30-180 minutes
            "budget": round(random.uniform(0, 100), 2),  # 0-100 USD
            "people": random.randint(1, 6),  # 1-6 people
            "history": []
        }
    return users

def generate_activities():
    moods = ["happy", "tired", "adventurous", "relaxed", "social"]
    activities = [
        {"name": "Watch a Comedy Movie", "duration": 90, "cost": 10.0, "people": 1, "mood": "happy", "description": "Laugh out loud with a funny movie at home or in a theater."},
        {"name": "Take a Nap", "duration": 30, "cost": 0.0, "people": 1, "mood": "tired", "description": "Rest and recharge with a short nap."},
        {"name": "Go Hiking", "duration": 120, "cost": 5.0, "people": 2, "mood": "adventurous", "description": "Explore a nearby trail and enjoy nature."},
        {"name": "Meditate", "duration": 20, "cost": 0.0, "people": 1, "mood": "relaxed", "description": "Find inner peace with a guided meditation session."},
        {"name": "Board Game Night", "duration": 60, "cost": 0.0, "people": 4, "mood": "social", "description": "Gather friends for a fun board game session."},
        {"name": "Visit a Museum", "duration": 90, "cost": 15.0, "people": 2, "mood": "happy", "description": "Explore art or history at a local museum."},
        {"name": "Read a Book", "duration": 60, "cost": 0.0, "people": 1, "mood": "tired", "description": "Dive into a novel or non-fiction at home."},
        {"name": "Rock Climbing", "duration": 60, "cost": 20.0, "people": 2, "mood": "adventurous", "description": "Challenge yourself at an indoor climbing gym."},
        {"name": "Spa Day", "duration": 120, "cost": 50.0, "people": 1, "mood": "relaxed", "description": "Pamper yourself with a spa treatment."},
        {"name": "Karaoke Night", "duration": 90, "cost": 10.0, "people": 4, "mood": "social", "description": "Sing your heart out with friends."},
        {"name": "Picnic in the Park", "duration": 60, "cost": 5.0, "people": 3, "mood": "happy", "description": "Enjoy a meal outdoors with friends or family."},
        {"name": "Listen to a Podcast", "duration": 45, "cost": 0.0, "people": 1, "mood": "tired", "description": "Relax with an engaging podcast episode."},
        {"name": "Kayaking", "duration": 90, "cost": 25.0, "people": 2, "mood": "adventurous", "description": "Paddle on a nearby lake or river."},
        {"name": "Yoga Session", "duration": 45, "cost": 5.0, "people": 1, "mood": "relaxed", "description": "Stretch and unwind with a yoga class."},
        {"name": "Trivia Night", "duration": 60, "cost": 5.0, "people": 4, "mood": "social", "description": "Test your knowledge at a local pub quiz."},
        {"name": "Bake Cookies", "duration": 60, "cost": 5.0, "people": 2, "mood": "happy", "description": "Have fun baking sweet treats at home."},
        {"name": "Watch a Sunset", "duration": 30, "cost": 0.0, "people": 1, "mood": "tired", "description": "Relax while watching a beautiful sunset."},
        {"name": "Bike Tour", "duration": 90, "cost": 10.0, "people": 2, "mood": "adventurous", "description": "Cycle through scenic routes in your area."},
        {"name": "Massage", "duration": 60, "cost": 40.0, "people": 1, "mood": "relaxed", "description": "Relieve stress with a professional massage."},
        {"name": "Dance Party", "duration": 60, "cost": 0.0, "people": 4, "mood": "social", "description": "Dance to your favorite tunes with friends."},
        {"name": "Visit a Farmers Market", "duration": 60, "cost": 10.0, "people": 2, "mood": "happy", "description": "Shop for fresh produce and local goods."},
        {"name": "Journaling", "duration": 30, "cost": 0.0, "people": 1, "mood": "tired", "description": "Reflect on your day with a journaling session."},
        {"name": "Ziplining", "duration": 60, "cost": 30.0, "people": 2, "mood": "adventurous", "description": "Experience an adrenaline rush with ziplining."},
        {"name": "Hot Bath", "duration": 30, "cost": 0.0, "people": 1, "mood": "relaxed", "description": "Soak in a warm bath to unwind."},
        {"name": "Movie Marathon", "duration": 120, "cost": 0.0, "people": 3, "mood": "social", "description": "Watch a series of movies with friends."},
        {"name": "Photography Walk", "duration": 60, "cost": 0.0, "people": 1, "mood": "happy", "description": "Capture beautiful moments in your neighborhood."},
        {"name": "Deep Breathing Exercises", "duration": 15, "cost": 0.0, "people": 1, "mood": "tired", "description": "Calm your mind with breathing exercises."},
        {"name": "Camping Trip", "duration": 120, "cost": 20.0, "people": 3, "mood": "adventurous", "description": "Spend time in nature with a camping adventure."},
        {"name": "Aromatherapy", "duration": 30, "cost": 5.0, "people": 1, "mood": "relaxed", "description": "Use essential oils to create a calming atmosphere."},
        {"name": "Potluck Dinner", "duration": 90, "cost": 5.0, "people": 5, "mood": "social", "description": "Share dishes with friends at a potluck."}
    ]
    return {f"activity{i+1}": activity for i, activity in enumerate(activities)}

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
def main():
    ensure_directory()
    user_prefs = generate_user_preferences()
    activities = generate_activities()
    save_json("data/user_preferences.json", user_prefs)
    save_json("data/activities.json", activities)
    print("Generated user_preferences.json and activities.json")

if __name__ == "__main__":
    main()