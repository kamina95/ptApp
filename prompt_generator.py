import json
import os

from flask import jsonify

DATA_FILE = 'data_test.json'
DATA_USER_FILE = 'data_user.json'


def get_all_exercises():
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

    return all_responses


def get_user_data():
    if os.path.exists(DATA_USER_FILE):
        with open(DATA_USER_FILE, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    return existing_data

def generate_prompt(user_prompt):
    prompt = "";
    exercises = get_all_exercises()
    user_data = get_user_data()

    return prompt
