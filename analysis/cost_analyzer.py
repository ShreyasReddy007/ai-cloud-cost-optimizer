from llm.recommendations import generate_recommendations


def analyze_costs(project_profile: dict, billing_data: list) -> dict:
    return generate_recommendations(project_profile, billing_data)
