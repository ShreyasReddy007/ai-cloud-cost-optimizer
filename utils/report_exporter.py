from pathlib import Path


def export_html_report(report: dict) -> str:
    """
    Safely exports cost optimization report as HTML.
    Always writes to the 'outputs/' directory.
    """

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)  # SAFE: always exists

    output_path = output_dir / "cost_optimization_report.html"

    analysis = report.get("analysis", {})
    recommendations = report.get("recommendations", [])

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Cloud Cost Optimization Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f9f9f9;
        }}
        h1, h2 {{
            color: #2c3e50;
        }}
        .box {{
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        th {{
            background-color: #ecf0f1;
        }}
        .rec {{
            background: #ffffff;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>

<h1>AI Cloud Cost Optimization Report</h1>

<div class="box">
    <h2>Project Summary</h2>
    <p><strong>Project:</strong> {report.get("project_name", "N/A")}</p>
    <p><strong>Total Monthly Cost:</strong> ₹{analysis.get("total_monthly_cost", "N/A")}</p>
    <p><strong>Budget:</strong> ₹{analysis.get("budget", "N/A")}</p>
    <p><strong>Over Budget:</strong> {analysis.get("is_over_budget", "N/A")}</p>
</div>

<div class="box">
    <h2>Cost Breakdown</h2>
    <table>
        <tr>
            <th>Service</th>
            <th>Monthly Cost (₹)</th>
        </tr>
"""

    for service, cost in analysis.get("service_costs", {}).items():
        html += f"""
        <tr>
            <td>{service}</td>
            <td>{cost}</td>
        </tr>
"""

    html += """
    </table>
</div>

<h2>Optimization Recommendations</h2>
"""

    for i, rec in enumerate(recommendations, start=1):
        html += f"""
<div class="rec">
    <h3>{i}. {rec.get("title", "N/A")}</h3>
    <p><strong>Service:</strong> {rec.get("service", "N/A")}</p>
    <p><strong>Potential Savings:</strong> ₹{rec.get("potential_savings", 0)}</p>
    <p><strong>Providers:</strong> {", ".join(rec.get("cloud_providers", []))}</p>
    <p>{rec.get("description", "")}</p>
</div>
"""

    html += """
</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")
    return str(output_path)
