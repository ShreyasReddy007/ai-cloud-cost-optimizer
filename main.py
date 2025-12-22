from cli.cli import show_menu
from utils.file_io import (
    write_text_file,
    write_json_file,
    read_text_file,
    read_json_file
)

from llm.profile_extractor import extract_project_profile
from llm.billing_generator import generate_mock_billing
from analysis.cost_analyzer import analyze_costs
from llm.recommendations import generate_recommendations
from utils.report_exporter import export_html_report



def main():
    while True:
        choice = show_menu()

        # Option 1: Enter project description
        if choice == "1":
            description = input("\nEnter project description:\n")
            write_text_file("project_description.txt", description)

            profile = extract_project_profile(description)
            write_json_file("project_profile.json", profile)

            print("\n✅ Project profile generated successfully.")

        # Option 2: Run complete cost analysis
        elif choice == "2":
            profile = read_json_file("project_profile.json")

            # Phase 2: Billing generation
            billing = generate_mock_billing(profile)
            write_json_file("mock_billing.json", billing)

            # Phase 3: Cost analysis
            analysis = analyze_costs(profile, billing)

            # Phase 3: Recommendations (LLM-driven)
            recommendations = generate_recommendations(profile, analysis)

            # Final combined report
            final_report = {
                "project_name": profile["name"],
                "analysis": analysis,
                "recommendations": recommendations,
                "summary": {
                    "total_potential_savings": sum(
                        r.get("potential_savings", 0)
                        for r in recommendations
                        if isinstance(r, dict)
                    ),

                    "recommendations_count": len(recommendations)
                }
            }

            write_json_file("cost_optimization_report.json", final_report)

            print("\n✅ Cost analysis and optimization report generated.")

        # Option 3: View recommendations
        elif choice == "3":
            report = read_json_file("cost_optimization_report.json")

            print("\n📊 Cost Optimization Summary")
            print("--------------------------------")
            print(f"Project: {report['project_name']}")
            print(f"Total Monthly Cost: {report['analysis']['total_monthly_cost']}")
            print(f"Budget: {report['analysis']['budget']}")
            print(f"Over Budget: {report['analysis']['is_over_budget']}")
            print("\nTop Recommendations:\n")

            for idx, rec in enumerate(report["recommendations"], start=1):
                print(f"{idx}. {rec['title']}")
                print(f"   Service: {rec['service']}")
                print(f"   Potential Savings: {rec['potential_savings']}")
                print(f"   Providers: {', '.join(rec['cloud_providers'])}")
                print()

        # Option 4: Export report (future extension)
        elif choice == "4":
            report = read_json_file("cost_optimization_report.json")
            path = export_html_report(report)
            print(f"\n📄 HTML report exported successfully: {path}")

        # Option 5: Exit
        elif choice == "5":
            print("\n👋 Exiting AI Cloud Cost Optimizer.")
            break


if __name__ == "__main__":
    main()
