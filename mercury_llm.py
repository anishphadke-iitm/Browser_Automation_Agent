import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MERCURY_API_KEY")

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

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    result = response.json()

    # Extract Mercury content
    content = result["choices"][0]["message"]["content"]

    # Convert text JSON → Python dict
    actions_json = json.loads(content)

    return actions_json