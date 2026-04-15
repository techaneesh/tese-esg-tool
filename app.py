"""
ESG Risk Analyzer — Streamlit Web UI
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd

from esg_analyzer import analyze_esg

# --- Page Config ---
st.set_page_config(
    page_title="ESG Risk Analyzer",
    page_icon="🌍",
    layout="wide",
)

# --- Custom Styling ---
st.markdown("""
<style>
    .risk-low { color: #2e7d32; font-weight: bold; font-size: 1.3em; }
    .risk-medium { color: #f9a825; font-weight: bold; font-size: 1.3em; }
    .risk-high { color: #e65100; font-weight: bold; font-size: 1.3em; }
    .risk-critical { color: #b71c1c; font-weight: bold; font-size: 1.3em; }
    .section-header { border-bottom: 2px solid #1b5e20; padding-bottom: 5px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("ESG Risk Analyzer")
st.caption("AI-powered sustainability risk assessment with finance-ready insights | Powered by Gemini 2.5 Flash")


def risk_color(level: str) -> str:
    colors = {"Low": "green", "Medium": "orange", "High": "red", "Critical": "violet"}
    return colors.get(level, "gray")


def display_result(result: dict):
    """Render a single ESG analysis result."""
    if "error" in result:
        st.error(f"Error: {result['error']}")
        return

    # --- Risk Level Header ---
    level = result.get("overall_risk_level", "Unknown")
    score = result.get("risk_score", 0)

    col_badge, col_score = st.columns([2, 1])
    with col_badge:
        risk_class = f"risk-{level.lower()}"
        st.markdown(f'<p class="{risk_class}">Overall Risk: {level.upper()}</p>', unsafe_allow_html=True)
    with col_score:
        st.metric("Risk Score", f"{score}/100")

    # --- Summary ---
    st.info(result.get("summary", "No summary available."))

    # --- E / S / G Columns ---
    col_e, col_s, col_g = st.columns(3)

    with col_e:
        st.subheader("Environmental")
        for risk in result.get("environmental_risks", []):
            severity = risk.get("severity", "Unknown")
            with st.expander(f"[{severity}] {risk['risk']}"):
                st.write(risk.get("description", ""))
                st.caption(f"Financial Impact: {risk.get('financial_impact', 'N/A')}")

    with col_s:
        st.subheader("Social")
        for item in result.get("social_considerations", []):
            st.markdown(f"- {item}")
        if not result.get("social_considerations"):
            st.caption("No social data provided — assessment recommended.")

    with col_g:
        st.subheader("Governance")
        for item in result.get("governance_considerations", []):
            st.markdown(f"- {item}")
        if not result.get("governance_considerations"):
            st.caption("No governance data provided — assessment recommended.")

    # --- Recommendations & Financing ---
    col_rec, col_fin = st.columns(2)

    with col_rec:
        st.subheader("Recommendations")
        for i, rec in enumerate(result.get("recommendations", []), 1):
            st.markdown(f"**{i}.** {rec}")

    with col_fin:
        st.subheader("Financing Opportunities")
        for item in result.get("financing_opportunities", []):
            st.success(f"{item}")
        if not result.get("financing_opportunities"):
            st.caption("No specific financing opportunities identified.")


# --- Sidebar: Input Mode ---
with st.sidebar:
    st.header("Input Data")
    input_mode = st.radio("Choose input method:", ["Upload CSV", "Manual Entry"])

    if input_mode == "Upload CSV":
        uploaded_file = st.file_uploader("Upload company sustainability CSV", type=["csv"])
        st.caption("CSV must have columns: company_name, industry, carbon_emissions_tons, energy_usage_kwh, water_consumption_liters, waste_generated_tons, renewable_energy_pct")

        # Show sample download
        sample_df = pd.read_csv("sample_data/sample_companies.csv")
        st.download_button(
            "Download Sample CSV",
            sample_df.to_csv(index=False),
            "sample_companies.csv",
            "text/csv",
        )

    else:
        st.subheader("Company Details")
        company_name = st.text_input("Company Name", value="Acme Corp")
        industry = st.selectbox(
            "Industry",
            ["Technology", "Manufacturing", "Retail", "Energy", "Agriculture", "Other"],
        )
        carbon = st.number_input("Carbon Emissions (tons CO2e/year)", min_value=0.0, value=3000.0, step=100.0)
        energy = st.number_input("Energy Usage (kWh/year)", min_value=0.0, value=1000000.0, step=50000.0)
        water = st.number_input("Water Consumption (liters/year)", min_value=0.0, value=200000.0, step=10000.0)
        waste = st.number_input("Waste Generated (tons/year)", min_value=0.0, value=300.0, step=10.0)
        renewable = st.slider("Renewable Energy %", 0, 100, 30)

        analyze_btn = st.button("Analyze ESG Risk", type="primary", use_container_width=True)

# --- Main Content ---
if input_mode == "Upload CSV" and uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader(f"Analyzing {len(df)} companies...")
    st.dataframe(df, use_container_width=True)

    if st.button("Run ESG Analysis", type="primary"):
        for _, row in df.iterrows():
            company_data = row.to_dict()
            with st.spinner(f"Analyzing {company_data['company_name']}..."):
                try:
                    result = analyze_esg(company_data)
                    result["company_name"] = company_data["company_name"]
                except Exception as e:
                    result = {"company_name": company_data.get("company_name", "Unknown"), "error": str(e)}

            st.divider()
            st.subheader(f"{result.get('company_name', 'Company')}")
            display_result(result)

elif input_mode == "Manual Entry" and analyze_btn:
    company_data = {
        "company_name": company_name,
        "industry": industry,
        "carbon_emissions_tons": carbon,
        "energy_usage_kwh": energy,
        "water_consumption_liters": water,
        "waste_generated_tons": waste,
        "renewable_energy_pct": renewable,
    }
    with st.spinner("Analyzing ESG risks..."):
        try:
            result = analyze_esg(company_data)
            result["company_name"] = company_name
        except Exception as e:
            result = {"company_name": company_name, "error": str(e)}

    st.divider()
    display_result(result)

else:
    # Landing state
    st.markdown("---")
    st.markdown("""
    ### How to use
    1. **Upload a CSV** with company sustainability data, or **enter data manually** in the sidebar
    2. Click **Analyze** to generate an AI-powered ESG risk summary
    3. Review environmental risks, social/governance considerations, and **financing opportunities**

    ### What you get
    - **Risk Level & Score** — Overall ESG risk assessment (Low/Medium/High/Critical)
    - **Environmental Risks** — Detailed breakdown with severity and financial impact
    - **Social & Governance** — Inferred considerations from environmental patterns
    - **Recommendations** — Actionable steps prioritized by impact
    - **Financing Opportunities** — Green bonds, sustainability-linked loans, carbon credits eligibility
    """)
