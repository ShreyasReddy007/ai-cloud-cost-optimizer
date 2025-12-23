from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def export_pdf_report(report: dict) -> str:
    """
    Exports the cost optimization report as a PDF.
    Always writes to outputs/cost_optimization_report.pdf
    """

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "cost_optimization_report.pdf"

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    x_margin = 1 * inch
    y = height - 1 * inch

    def draw_line(text):
        nonlocal y
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch
        c.drawString(x_margin, y, text)
        y -= 14

    # Title
    c.setFont("Helvetica-Bold", 16)
    draw_line("AI Cloud Cost Optimization Report")
    y -= 10

    # Project Summary
    c.setFont("Helvetica-Bold", 12)
    draw_line("Project Summary")

    c.setFont("Helvetica", 10)
    analysis = report.get("analysis", {})

    draw_line(f"Project Name: {report.get('project_name', 'N/A')}")
    draw_line(f"Total Monthly Cost: ₹{analysis.get('total_monthly_cost', 'N/A')}")
    draw_line(f"Budget: ₹{analysis.get('budget', 'N/A')}")
    draw_line(f"Over Budget: {analysis.get('is_over_budget', 'N/A')}")
    y -= 10

    # Cost Breakdown
    c.setFont("Helvetica-Bold", 12)
    draw_line("Cost Breakdown by Service")

    c.setFont("Helvetica", 10)
    for service, cost in analysis.get("service_costs", {}).items():
        draw_line(f"- {service}: ₹{cost}")
    y -= 10
 
    # Recommendations
    c.setFont("Helvetica-Bold", 12)
    draw_line("Optimization Recommendations")

    c.setFont("Helvetica", 10)
    recommendations = report.get("recommendations", [])

    for idx, rec in enumerate(recommendations, start=1):
        draw_line(f"{idx}. {rec.get('title', 'N/A')}")
        draw_line(f"   Service: {rec.get('service', 'N/A')}")
        draw_line(f"   Potential Savings: ₹{rec.get('potential_savings', 0)}")
        draw_line(f"   Providers: {', '.join(rec.get('cloud_providers', []))}")
        y -= 6

    c.save()
    return str(output_path)
