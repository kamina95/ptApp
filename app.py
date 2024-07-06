from flask import Flask, request, jsonify
import openai
import os
import json
from dotenv import load_dotenv

import openai_call

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

DATA_FILE = 'data.json'


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


@app.route('/input_data', methods=['POST'])
def input_data():
    data = request.json
    content = data.get('content')
    response = openai_call.call_openai(content)
    json.dump(response, open('data_test.json', 'w'))
    return jsonify({"message": "Data added successfully"}), 200


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
