# ESG Risk Analyzer

AI-powered tool that analyzes company sustainability data and generates finance-ready ESG risk summaries using Google Gemini 2.5 Flash.

Built as part of the AI Engineer assignment for [Tese.io](https://tese.io) — a climate & nature strategy platform that turns sustainability data into finance-ready action.

## Features

- **AI-Powered Analysis**: Uses Gemini 2.5 Flash to generate contextual ESG risk assessments
- **Industry Benchmarking**: Compares company metrics against industry-specific benchmarks
- **Finance-Ready Insights**: Identifies green financing opportunities (green bonds, carbon credits, EU taxonomy alignment)
- **Structured Output**: Risk levels (Low/Medium/High/Critical), scored 0-100, with detailed breakdowns
- **Dual Interface**: CLI for quick analysis + Streamlit web UI for interactive exploration
- **Batch Processing**: Upload CSV to analyze multiple companies at once

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

```bash
cp .env.example .env
# Edit .env and add your Google Gemini API key
```

Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 3. Run

**CLI — Batch mode (from CSV):**
```bash
python cli.py --file sample_data/sample_companies.csv
```

**CLI — Interactive mode:**
```bash
python cli.py --interactive
```

**Streamlit Web UI:**
```bash
streamlit run app.py
```

## Input Format

The tool accepts sustainability data with these fields:

| Field | Description | Example |
|-------|-------------|---------|
| `company_name` | Company name | Acme Corp |
| `industry` | Industry sector | Technology, Manufacturing, Retail, Energy, Agriculture |
| `carbon_emissions_tons` | Annual CO2 emissions in tons | 2500 |
| `energy_usage_kwh` | Annual energy usage in kWh | 1200000 |
| `water_consumption_liters` | Annual water consumption in liters | 50000 |
| `waste_generated_tons` | Annual waste generated in tons | 150 |
| `renewable_energy_pct` | Renewable energy percentage (0-100) | 85 |

A sample CSV with 5 companies across different industries is included in `sample_data/sample_companies.csv`.

## Output Structure

The tool generates a structured ESG risk summary containing:

- **Overall Risk Level**: Low / Medium / High / Critical (scored 0-100)
- **Environmental Risks**: Specific risks with severity, description, and financial impact
- **Social Considerations**: Inferred social risks from environmental patterns
- **Governance Considerations**: Inferred governance risks
- **Recommendations**: Actionable steps prioritized by impact
- **Financing Opportunities**: Green bonds, sustainability-linked loans, carbon credits eligibility
- **Executive Summary**: Finance-ready summary for decision-makers

## Tech Stack

- **Python 3.10+**
- **Google Gemini 2.5 Flash** — LLM for ESG analysis
- **Streamlit** — Web UI
- **pandas** — CSV data handling
- **python-dotenv** — Environment variable management

## Project Structure

```
tese-esg-tool/
├── app.py                    # Streamlit web UI
├── esg_analyzer.py           # Core analysis engine
├── cli.py                    # CLI interface
├── sample_data/
│   └── sample_companies.csv  # Sample sustainability data
├── requirements.txt
├── .env.example
├── AI_PROMPTS.md             # AI prompts used during development
└── README.md
```

## Author

Aneesh Mishra
