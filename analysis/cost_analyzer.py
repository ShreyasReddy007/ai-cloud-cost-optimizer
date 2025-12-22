from collections import defaultdict


def analyze_costs(project_profile: dict, billing_data: list) -> dict:
    service_costs = defaultdict(float)
    total_cost = 0.0

    for record in billing_data:
        service = record["service"]
        cost = record["cost_inr"]
        service_costs[service] += cost
        total_cost += cost

    budget = project_profile["budget_inr_per_month"]
    budget_variance = total_cost - budget
    is_over_budget = total_cost > budget

    # Identify high-cost services (>30% of total)
    high_cost_services = {
        svc: cost
        for svc, cost in service_costs.items()
        if cost / total_cost > 0.3
    }

    return {
        "total_monthly_cost": round(total_cost, 2),
        "budget": budget,
        "budget_variance": round(budget_variance, 2),
        "is_over_budget": is_over_budget,
        "service_costs": dict(service_costs),
        "high_cost_services": high_cost_services
    }
