import os
import json
import requests
from dotenv import load_dotenv

from utils.json_validator import validate_json

load_dotenv()

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


PROJECT_PROFILE_SCHEMA = {
    "type": "object",
    "required": [
        "name",
        "budget_inr_per_month",
        "description",
        "tech_stack",
        "non_functional_requirements"
    ],
    "properties": {
        "name": {"type": "string"},
        "budget_inr_per_month": {"type": "number"},
        "description": {"type": "string"},
        "tech_stack": {
            "type": "object",
            "properties": {
                "frontend": {"type": ["string", "null"]},
                "backend": {"type": ["string", "null"]},
                "database": {"type": ["string", "null"]},
                "hosting": {"type": ["string", "null"]},
                "proxy": {"type": ["string", "null"]}
            }
        },
        "non_functional_requirements": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}


def _call_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a strict JSON generator. "
                    "Return ONLY valid JSON. "
                    "Do not include explanations or markdown."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 600
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

import re
import json
def extract_project_profile(project_description: str) -> dict:
    prompt = f"""
From the following project description, extract a structured project profile.

Rules:
- Output ONLY valid JSON
- Fill missing fields with null or empty lists
- If the project description explicitly mentions a numeric budget,
  you MUST use that exact value.
- Do NOT infer, estimate, or adjust the budget.

JSON format:
{{
  "name": string,
  "budget_inr_per_month": number,
  "description": string,
  "tech_stack": {{
    "frontend": string | null,
    "backend": string | null,
    "database": string | null,
    "hosting": string | null,
    "proxy": string | null
  }},
  "non_functional_requirements": [string]
}}

Project description:
\"\"\"
{project_description}
\"\"\"
"""

    raw_output = _call_llm(prompt)

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON.\nRaw output:\n{raw_output}"
        ) from e

    # ---- HARD SAFETY: enforce explicit user budget ----
    match = re.search(r'(\d+)\s*INR', project_description, re.IGNORECASE)
    if match:
        explicit_budget = int(match.group(1))
        data["budget_inr_per_month"] = explicit_budget

    validate_json(data, PROJECT_PROFILE_SCHEMA)
    return data