"""
ESG Risk Analyzer — Core Engine
Analyzes company sustainability data and generates finance-ready ESG risk summaries
using Google Gemini 2.5 Flash.
"""

import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a senior ESG (Environmental, Social, Governance) analyst specializing in SME climate risk assessment and sustainable finance advisory. Your role is to analyze company sustainability data and produce actionable, finance-ready ESG risk summaries.

When analyzing data, you must:
1. Compare the company's metrics against industry benchmarks (provided below).
2. Assess environmental risks with specific financial implications (regulatory exposure, carbon pricing, stranded asset risk).
3. Infer potential social and governance considerations from environmental data patterns.
4. Identify green financing opportunities (green bonds, sustainability-linked loans, carbon credits, EU taxonomy alignment).
5. Provide concrete, actionable recommendations prioritized by impact.

Industry Benchmarks (annual, mid-size company):
- Technology: ~2,500 tCO2, ~1,200,000 kWh, ~50,000 L water, ~150 t waste, ~60-85% renewable
- Manufacturing: ~8,000-12,000 tCO2, ~2,000,000 kWh, ~800,000 L water, ~500-800 t waste, ~10-20% renewable
- Retail: ~3,000-4,000 tCO2, ~1,500,000 kWh, ~100,000-150,000 L water, ~300-500 t waste, ~20-35% renewable
- Energy: ~10,000-20,000 tCO2, ~800,000 kWh, ~200,000 L water, ~150-300 t waste, ~30-98% renewable (varies widely)
- Agriculture: ~300-500 tCO2, ~80,000-120,000 kWh, ~2,000,000-3,000,000 L water, ~50-100 t waste, ~3-10% renewable

You MUST respond with valid JSON only — no markdown, no code fences, no explanatory text outside the JSON structure."""

USER_PROMPT_TEMPLATE = """Analyze the following company's sustainability data and generate a comprehensive ESG risk summary.

Company: {company_name}
Industry: {industry}
Annual Carbon Emissions: {carbon_emissions_tons} tons CO2e
Annual Energy Usage: {energy_usage_kwh} kWh
Annual Water Consumption: {water_consumption_liters} liters
Annual Waste Generated: {waste_generated_tons} tons
Renewable Energy Percentage: {renewable_energy_pct}%

Respond in this exact JSON structure:
{{
    "overall_risk_level": "Low | Medium | High | Critical",
    "risk_score": <integer 0-100, where 100 is highest risk>,
    "environmental_risks": [
        {{
            "risk": "<specific risk name>",
            "severity": "Low | Medium | High | Critical",
            "description": "<1-2 sentence explanation>",
            "financial_impact": "<specific financial implication>"
        }}
    ],
    "social_considerations": [
        "<inferred social risk or consideration based on environmental patterns>"
    ],
    "governance_considerations": [
        "<inferred governance risk or consideration>"
    ],
    "recommendations": [
        "<specific, actionable recommendation with expected impact>"
    ],
    "financing_opportunities": [
        "<specific green financing instrument or program the company may qualify for>"
    ],
    "summary": "<3-4 sentence executive summary highlighting key risks and opportunities, framed for financial decision-makers>"
}}"""


def _get_model():
    """Initialize and return the Gemini model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Set it in your .env file or environment variables."
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=genai.GenerationConfig(
            temperature=0.3,
            max_output_tokens=4096,
        ),
        system_instruction=SYSTEM_PROMPT,
    )


def analyze_esg(company_data: dict) -> dict:
    """
    Analyze a company's sustainability data and return an ESG risk summary.

    Args:
        company_data: Dict with keys: company_name, industry, carbon_emissions_tons,
                      energy_usage_kwh, water_consumption_liters, waste_generated_tons,
                      renewable_energy_pct

    Returns:
        Dict with ESG risk analysis including risk_level, environmental_risks,
        social/governance considerations, recommendations, and financing opportunities.
    """
    required_fields = [
        "company_name", "industry", "carbon_emissions_tons",
        "energy_usage_kwh", "water_consumption_liters",
        "waste_generated_tons", "renewable_energy_pct",
    ]
    missing = [f for f in required_fields if f not in company_data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    prompt = USER_PROMPT_TEMPLATE.format(**company_data)
    model = _get_model()
    response = model.generate_content(prompt)

    # Parse JSON from response — handle potential markdown fences
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]  # remove first line (```json)
        text = text.rsplit("```", 1)[0]  # remove closing ```
        text = text.strip()

    # Fix trailing commas that Gemini sometimes adds (invalid JSON)
    text = re.sub(r",\s*([}\]])", r"\1", text)

    try:
        result = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse Gemini response as JSON: {e}\nRaw response: {text[:500]}"
        )

    return result


def analyze_batch(companies: list[dict]) -> list[dict]:
    """Analyze multiple companies and return list of results."""
    results = []
    for company in companies:
        try:
            result = analyze_esg(company)
            result["company_name"] = company["company_name"]
            results.append(result)
        except Exception as e:
            results.append({
                "company_name": company.get("company_name", "Unknown"),
                "error": str(e),
            })
    return results
