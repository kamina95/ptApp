from flask import jsonify


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