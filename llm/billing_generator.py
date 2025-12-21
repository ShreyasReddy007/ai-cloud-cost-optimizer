def generate_mock_billing(project_profile: dict) -> list:
    return [
        {
            "month": "2025-01",
            "service": "Compute",
            "usage_quantity": 720,
            "unit": "hours",
            "cost_inr": 1500,
            "region": "ap-south-1",
            "desc": "Backend server"
        }
    ]
