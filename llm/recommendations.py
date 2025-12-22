import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


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
                    "You are a cloud cost optimization expert. "
                    "You must output ONLY valid JSON. "
                    "The output MUST be a JSON ARRAY. "
                    "No explanations. No markdown."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1500
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def generate_recommendations(project_profile: dict, analysis: dict) -> list:
    base_prompt = f"""
Generate 6 to 10 cloud cost optimization recommendations.

STRICT RULES:
- Output ONLY valid JSON
- Output MUST be a JSON ARRAY
- 6 to 10 items
- Include AWS, Azure, GCP
- Include open-source or free-tier alternatives
- Each recommendation MUST include:
  title, service, current_cost, potential_savings,
  recommendation_type, description,
  implementation_effort, risk_level, cloud_providers

Cost analysis:
{json.dumps(analysis, indent=2)}

Project profile:
{json.dumps(project_profile, indent=2)}
"""

    last_error = None

    for attempt in range(3):
        raw_output = _call_llm(base_prompt)

        try:
            data = json.loads(raw_output)

            if not isinstance(data, list):
                raise ValueError("LLM output is not a JSON array")

            return data

        except Exception as e:
            last_error = e
            base_prompt += (
                "\nREMINDER: Output must be a COMPLETE JSON ARRAY only."
            )

    raise ValueError(
        "LLM failed to generate valid recommendations after retries.\n"
        f"Last error: {last_error}"
    )
