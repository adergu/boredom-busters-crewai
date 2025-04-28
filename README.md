# Boredom Busters

**Boredom Busters** is a Python-based intelligent system designed to combat boredom by suggesting personalized activities based on a user's mood, time availability, budget, and group size. Built using the **CrewAI** framework and powered by the **Groq API** (LLaMA3-70B model), it leverages AI agents to analyze user input, validate constraints, and recommend tailored activities. The system saves user preferences and activity history in JSON files and provides performance metrics based on user feedback.

## Features
- **Mood Analysis**: Interprets user responses to categorize mood (happy, tired, adventurous, relaxed, social).
- **Constraint Validation**: Ensures budget, time, and group size are within valid ranges.
- **Activity Recommendations**: Suggests 3-5 activities matching user preferences from a predefined list.
- **User Feedback**: Collects ratings (1-5) and calculates metrics (User Feedback, Relevance Score, Activity Effectiveness Score).
- **Data Persistence**: Stores user preferences and history in `data/user_preferences.json` and activity details in `data/activities.json`.

## Prerequisites
- **Python**: Version 3.12 (recommended; Python 3.13 may have compatibility issues with some dependencies).
- **Groq API Key**: Obtain from [Groq Console](https://console.groq.com).
- **Virtual Environment**: Recommended for dependency isolation.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd boredom-busters-crewai
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**:
   Ensure `requirements.txt` is present, then run:
   ```bash
   pip install -r requirements.txt
   ```
   **requirements.txt**:
   ```
   crewai==0.76.0
   groq==0.9.0
   python-dotenv==1.0.1
   httpx==0.27.0
   tenacity==8.5.0
   langchain-groq==0.3.0
   pydantic==2.9.2
   litellm==1.48.8
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root:
   ```plaintext
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Replace `your_groq_api_key_here` with your Groq API key.

5. **Generate JSON Files**:
   Run `generate_json.py` to create `data/user_preferences.json` (50 users) and `data/activities.json` (30 activities):
   ```bash
   python generate_json.py
   ```

## Usage
1. **Run the Application**:
   ```bash
   python src/main.py
   ```
   The program displays a menu:
   ```
   === Boredom Busters ===
   1. Save Preferences
   2. Get Activity Suggestions
   3. Exit
   Choose an option:
   ```

2. **Save Preferences** (Option 1):
   - Enter a user ID (e.g., `user51`).
   - Answer prompts for mood, budget, time, and group size.
   - Example:
     ```
     Enter user ID (e.g., user1): user51
     How you doin' today? (e.g., feeling great, kinda tired): tired
     How was your day so far? (e.g., awesome, stressful): stressful
     What's your budget? (e.g., 20, or 0 for none): 10
     How much time do you have? (minutes, e.g., 60): 60
     How many people? (e.g., 1 for solo, 2 for couple): 2
     Mood interpreted as: tired
     Preferences saved successfully.
     ```
   - Updates `data/user_preferences.json`.

3. **Get Activity Suggestions** (Option 2):
   - Enter a user ID (must exist in `data/user_preferences.json`).
   - Receive 3-5 activity suggestions with details (name, duration, cost, people, mood, description).
   - Rate the suggestions (1-5).
   - Example:
     ```
     Enter user ID (e.g., user1): user1
     Activity Suggestions:
     1. Watch a Sunset (30 min, $0.0, 1 people)
        Relax while watching a beautiful sunset.
     2. Journaling (30 min, $0.0, 1 people)
        Reflect on your day with a journaling session.
     3. Deep Breathing Exercises (15 min, $0.0, 1 people)
        Calm your mind with breathing exercises.
     Rate these suggestions (1-5): 4
     Performance Metrics:
     User Feedback (UF): 0.80
     Relevance Score (RS): 0.75
     Activity Effectiveness Score (AES): 0.78
     Result: Bad
     Feedback saved.
     ```
   - Updates `data/user_preferences.json` with history and metrics.

4. **Exit** (Option 3):
   - Closes the application.

## File Structure
```
boredom-busters-crewai/
├── agents/
│   ├── mood_analyzer.py       # Mood Analyzer agent
│   ├── info_collector.py      # Info Collector agent
│   ├── activity_recommender.py # Activity Recommender agent
├── data/
│   ├── user_preferences.json  # User preferences and history
│   ├── activities.json        # Predefined activities
├── tasks/
│   ├── tasks.py               # Task definitions
├── src/
│   ├── main.py                # Main application
├── venv/                      # Virtual environment
├── .env                       # Environment variables (GROQ_API_KEY)
├── .gitignore                 # Git ignore file
├── requirements.txt           # Dependencies
├── generate_json.py           # Generates JSON data
└── README.md                  # Project documentation
```

## Dependencies
- **crewai (0.76.0)**: Framework for AI agent orchestration.
- **groq (0.9.0)**: Groq API client for LLM access.
- **langchain-groq (0.3.0)**: LangChain integration for Groq.
- **python-dotenv (1.0.1)**: Loads environment variables.
- **httpx (0.27.0)**: HTTP client for API calls.
- **tenacity (8.5.0)**: Retry logic for API calls.
- **pydantic (2.9.2)**: Data validation.
- **litellm (1.48.8)**: Lightweight LLM interface.

## Troubleshooting
- **Error: `litellm.BadRequestError: LLM Provider NOT provided`**:
  - Ensure agent files (`agents/*.py`) use `model_name="groq/llama3-70b-8192"`.
  - Verify `GROQ_API_KEY` in `.env` is valid (regenerate at [Groq Console](https://console.groq.com) if needed).
  - Reinstall dependencies:
    ```bash
    pip uninstall -y crewai groq python-dotenv httpx tenacity langchain-groq pydantic litellm
    pip install -r requirements.txt
    ```
- **Error: `RetryError`**:
  - Indicates repeated API failures. Check Groq API status or key validity.
- **JSON Files Missing**:
  - Run `python generate_json.py` to create `data/user_preferences.json` and `data/activities.json`.
- **Python Version Issues**:
  - Use Python 3.12 if Python 3.13 causes compatibility issues:
    ```bash
    "C:\Program Files\Python\Python312\python.exe" -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
- **Invalid User ID**:
  - Ensure the user ID exists in `data/user_preferences.json` or save preferences first (Option 1).

## Future Enhancements
- **Geolocation Agent**: Add location-based activity suggestions (e.g., nearby parks or events).
- **Streamlit UI**:
  ```bash
  pip install streamlit
  ```
  Create a web interface for user interaction.
- **Additional Metrics**: Enhance performance metrics with more sophisticated calculations.
- **Activity Expansion**: Add more activities to `data/activities.json`.

## Contributing
- Fork the repository.
- Create a feature branch (`git checkout -b feature-name`).
- Commit changes (`git commit -m "Add feature"`).
- Push to the branch (`git push origin feature-name`).
- Open a pull request.

## License
This project is licensed under the MIT License.

## Contact
For issues or suggestions, open an issue on the repository or contact the project maintainers.

