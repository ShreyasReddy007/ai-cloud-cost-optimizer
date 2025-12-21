import os
import json
import requests
from dotenv import load_dotenv

from utils.json_validator import validate_json

load_dotenv()

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


MOCK_BILLING_SCHEMA = {
    "type": "array",
    "minItems": 12,
    "maxItems": 20,
    "items": {
        "type": "object",
        "required": [
            "month",
            "service",
            "resource_id",
            "region",
            "usage_type",
            "usage_quantity",
            "unit",
            "cost_inr",
            "desc"
        ],
        "properties": {
            "month": {"type": "string"},
            "service": {"type": "string"},
            "resource_id": {"type": "string"},
            "region": {"type": "string"},
            "usage_type": {"type": "string"},
            "usage_quantity": {"type": "number"},
            "unit": {"type": "string"},
            "cost_inr": {"type": "number"},
            "desc": {"type": "string"}
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
                    "You are a cloud billing data generator. "
                    "You must output ONLY valid JSON. "
                    "No explanations. No markdown."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 2500
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def generate_mock_billing(project_profile: dict) -> list:
    prompt = f"""
Generate realistic synthetic cloud billing data based on the following project profile.

STRICT RULES (MANDATORY):
- Output ONLY valid JSON
- Output an ARRAY of 12 to 20 records
- Monthly budget: {project_profile["budget_inr_per_month"]} INR
- Total cost MUST be between 1.2x and 1.8x of the budget
- Total cost MUST NOT exceed 2x the budget
- No single service should exceed ~40% of total cost

SERVICE DISTRIBUTION:
- Compute, Database, Storage, Networking, Monitoring

REALISM:
- Real cloud regions
- Realistic usage units
- Cloud-like resource IDs

Each record format:
{{
  "month": "YYYY-MM",
  "service": string,
  "resource_id": string,
  "region": string,
  "usage_type": string,
  "usage_quantity": number,
  "unit": string,
  "cost_inr": number,
  "desc": string
}}

Project profile:
{json.dumps(project_profile, indent=2)}
"""

    last_error = None

    for attempt in range(3):  # retry up to 3 times
        raw_output = _call_llm(prompt)

        try:
            data = json.loads(raw_output)
            validate_json(data, MOCK_BILLING_SCHEMA)
            return data
        except Exception as e:
            last_error = e
            # tighten instruction on retry
            prompt += "\nREMINDER: Output must be COMPLETE and valid JSON. Close the array properly."

    raise ValueError(
        f"LLM failed to generate valid billing JSON after retries.\nLast error: {last_error}"
    )
