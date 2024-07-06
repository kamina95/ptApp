from flask import Flask, request, jsonify
import openai
import os
import json
from dotenv import load_dotenv

import openai_call

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

DATA_FILE = 'data_test.json'


# Load data from JSON file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": []}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# Set up OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')


# Helper function to fetch user data
def get_user_data(user_id):
    data = load_data()
    for user in data["users"]:
        if user["id"] == user_id:
            return user
    return None


@app.route('/registration', methods=['POST'])
def registration():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    height = data.get('height')
    weight = data.get('weight')
    fat_percentage = data.get('fat_percentage')
    fitness_goals = data.get('fitness_goals')
    current_fitness_level = data.get('current_fitness_level')
    workout_preferences = data.get('workout_preferences')
    dietary_preferences = data.get('dietary_preferences')
    email = data.get('email')

    user_data = {
        "id": user_id,
        "name": name,
        "age": age,
        "gender" : gender,
        "height" : height,
        "weight" : weight,
        "fat_percentage" : fat_percentage,
        "fitness_goals" : fitness_goals,
        "current_fitness_level" : current_fitness_level,
        "workout_preferences" : workout_preferences,
        "dietary_preferences" : dietary_preferences,
        "email" : email
    }
    with open("user_data.json", 'w') as f:
        json.dump(user_data, f, indent=4)
    return jsonify({"message": "User registered successfully"}), 200


@app.route('/input_data', methods=['POST'])
def input_data():
    data = request.json
    content = data.get('content')
    response = openai_call.call_openai(content)

    # Load existing data from JSON file
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Ensure the existing data is a list
    if not isinstance(existing_data, list):
        existing_data = []

    # Append the new response to the existing data
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in the response"}), 400

    new_entry = {
        "content": content,
        "response": response_json  # Ensure the response is parsed from string to JSON
    }
    existing_data.append(new_entry)

    # Save the updated data back to the JSON file
    with open(DATA_FILE, 'w') as f:
        json.dump(existing_data, f, indent=4)

    print(response)
    return jsonify({"message": "Data added successfully"}), 200


@app.route('/get_all_responses', methods=['GET'])
def get_all_responses():
    # Load existing data from JSON file
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Extract and merge all responses into one JSON object
    all_responses = []
    for entry in existing_data:
        if isinstance(entry['response'], list):
            all_responses.extend(entry['response'])
        else:
            return jsonify({"error": "Invalid response format in stored data"}), 500

    return jsonify(all_responses), 200


@app.route('/add_workout', methods=['POST'])
def add_workout():
    data = request.json
    user_id = data.get('user_id')
    workout = data.get('workout')

    data_file = load_data()
    user = get_user_data(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if "workouts" not in user:
        user["workouts"] = []
    user["workouts"].append(workout)
    save_data(data_file)
    return jsonify({"message": "Workout added successfully"}), 200


@app.route('/get_recommendation/<user_id>', methods=['GET'])
def get_recommendation(user_id):
    user = get_user_data(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    workouts = user.get('workouts', [])
    goals = user.get('goals', {})

    # Create a prompt for OpenAI
    prompt = f"Based on the following workout data: {workouts}\nAnd goals: {goals}\nRecommend a new workout routine."

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )

    recommendation = response.choices[0].text.strip()
    return jsonify({"recommendation": recommendation}), 200


if __name__ == '__main__':
    app.run(debug=True)
