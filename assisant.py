import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')


def create_instructions_from_md(path):
    instruction_path = Path(path)
    return instruction_path.read_text()


# Step 1: Create an Assistant
my_assistant = client.beta.assistants.create(
    model="gpt-4o",
    instructions=create_instructions_from_md("data-input-assistant-instructions.txt"),
    name="Input Exercise Assistant",
    tools=[{"type": "code_interpreter"}]
)
print(f"This is the assistant object: {my_assistant} \n")

assistants_id = {
    "id": my_assistant.id
}

json.dump(assistants_id, open('data.json', 'w'))
