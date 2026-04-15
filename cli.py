"""
ESG Risk Analyzer — CLI Interface
Usage:
    python cli.py --file sample_data/sample_companies.csv
    python cli.py --interactive
"""

import argparse
import sys

import pandas as pd

from esg_analyzer import analyze_esg


def print_risk_badge(level: str) -> str:
    """Return a colored risk badge for terminal output."""
    badges = {
        "Low": "\033[92m[LOW RISK]\033[0m",
        "Medium": "\033[93m[MEDIUM RISK]\033[0m",
        "High": "\033[91m[HIGH RISK]\033[0m",
        "Critical": "\033[95m[CRITICAL RISK]\033[0m",
    }
    return badges.get(level, f"[{level}]")


def print_result(result: dict):
    """Pretty-print an ESG analysis result."""
    if "error" in result:
        print(f"\n  Error analyzing {result['company_name']}: {result['error']}")
        return

    print(f"\n{'='*70}")
    print(f"  {result.get('company_name', 'Company')}  {print_risk_badge(result['overall_risk_level'])}")
    print(f"  Risk Score: {result['risk_score']}/100")
    print(f"{'='*70}")

    # Summary
    print(f"\n  SUMMARY")
    print(f"  {result['summary']}")

    # Environmental Risks
    print(f"\n  ENVIRONMENTAL RISKS")
    for risk in result.get("environmental_risks", []):
        severity = risk.get("severity", "Unknown")
        print(f"    [{severity}] {risk['risk']}")
        print(f"           {risk.get('description', '')}")
        print(f"           Financial Impact: {risk.get('financial_impact', 'N/A')}")

    # Social Considerations
    if result.get("social_considerations"):
        print(f"\n  SOCIAL CONSIDERATIONS")
        for item in result["social_considerations"]:
            print(f"    - {item}")

    # Governance Considerations
    if result.get("governance_considerations"):
        print(f"\n  GOVERNANCE CONSIDERATIONS")
        for item in result["governance_considerations"]:
            print(f"    - {item}")

    # Recommendations
    print(f"\n  RECOMMENDATIONS")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"    {i}. {rec}")

    # Financing Opportunities
    if result.get("financing_opportunities"):
        print(f"\n  FINANCING OPPORTUNITIES")
        for item in result["financing_opportunities"]:
            print(f"    -> {item}")

    print()


def run_from_file(filepath: str):
    """Load companies from CSV and analyze each."""
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    print(f"\nLoaded {len(df)} companies from {filepath}")
    print("Analyzing ESG risks...\n")

    for _, row in df.iterrows():
        company_data = row.to_dict()
        try:
            result = analyze_esg(company_data)
            result["company_name"] = company_data["company_name"]
            print_result(result)
        except Exception as e:
            print(f"\n  Error analyzing {company_data.get('company_name', 'Unknown')}: {e}")


def run_interactive():
    """Collect company data interactively and analyze."""
    print("\n--- ESG Risk Analyzer (Interactive Mode) ---\n")

    company_data = {}
    company_data["company_name"] = input("Company Name: ").strip()
    company_data["industry"] = input("Industry (Technology/Manufacturing/Retail/Energy/Agriculture): ").strip()
    company_data["carbon_emissions_tons"] = float(input("Annual Carbon Emissions (tons CO2e): "))
    company_data["energy_usage_kwh"] = float(input("Annual Energy Usage (kWh): "))
    company_data["water_consumption_liters"] = float(input("Annual Water Consumption (liters): "))
    company_data["waste_generated_tons"] = float(input("Annual Waste Generated (tons): "))
    company_data["renewable_energy_pct"] = float(input("Renewable Energy Percentage (0-100): "))

    print("\nAnalyzing ESG risks...")
    result = analyze_esg(company_data)
    result["company_name"] = company_data["company_name"]
    print_result(result)


def main():
    parser = argparse.ArgumentParser(description="ESG Risk Analyzer — AI-powered sustainability assessment")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", help="Path to CSV file with company data")
    group.add_argument("--interactive", "-i", action="store_true", help="Enter data interactively")

    args = parser.parse_args()

    if args.file:
        run_from_file(args.file)
    elif args.interactive:
        run_interactive()


if __name__ == "__main__":
    main()
