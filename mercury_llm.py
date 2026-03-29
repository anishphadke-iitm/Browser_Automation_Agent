import requests
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MERCURY_API_KEY")


def clean_json(content):
    """
    Remove markdown code fences if Mercury returns ```json blocks.
    """
    content = re.sub(r"```json|```", "", content)
    return content.strip()


def get_actions_from_instruction(instruction):

    url = "https://api.inceptionlabs.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a browser automation planner.

Convert the user's instruction into browser actions.

Supported actions:

navigate → open URL  
click → click element  
fill → type text  
extract → get text  
wait → wait seconds  

Instruction:
{instruction}

Return ONLY JSON.

Example:

{{
"url": "https://example.com/login",
"actions": [
    {{"type": "navigate"}},
    {{
        "type": "fill",
        "selector": "#username",
        "text": "admin"
    }},
    {{
        "type": "fill",
        "selector": "#password",
        "text": "password"
    }},
    {{
        "type": "click",
        "selector": "button[type='submit']"
    }},
    {{
        "type": "wait",
        "seconds": 3
    }},
    {{
        "type": "extract",
        "selector": "h1"
    }}
]
}}
"""

    data = {
        "model": "mercury-2",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data
        )

        # Important fix
        response.raise_for_status()

        result = response.json()

        content = result["choices"][0]["message"]["content"]

        # Clean markdown fences
        cleaned = clean_json(content)

        actions_json = json.loads(cleaned)

        return actions_json

    except Exception as e:

        print("Mercury API Error:")
        print(e)

        raise RuntimeError(
            f"Failed to generate plan from Mercury: {e}"
        )