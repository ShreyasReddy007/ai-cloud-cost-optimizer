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


def main():
    while True:
        choice = show_menu()

        if choice == "1":
            description = input("\nEnter project description:\n")
            write_text_file("project_description.txt", description)

            profile = extract_project_profile(description)
            write_json_file("project_profile.json", profile)

            print("Project profile generated.")

        elif choice == "2":
            profile = read_json_file("project_profile.json")
            billing = generate_mock_billing(profile)
            write_json_file("mock_billing.json", billing)

            report = analyze_costs(profile, billing)
            write_json_file("cost_optimization_report.json", report)

            print("Cost analysis completed.")

        elif choice == "3":
            report = read_json_file("cost_optimization_report.json")
            print(report)

        elif choice == "4":
            print("Export feature coming in Phase 3.")

        elif choice == "5":
            print("Exiting.")
            break


if __name__ == "__main__":
    main()
