def generate_recommendations(project_profile: dict, billing_data: list) -> dict:
    total_cost = sum(item["cost_inr"] for item in billing_data)

    return {
        "project_name": project_profile["name"],
        "total_monthly_cost": total_cost,
        "recommendations": [
            {
                "title": "Use free tier where possible",
                "potential_savings": 500,
                "cloud_providers": ["AWS", "Azure", "GCP"]
            }
        ]
    }
