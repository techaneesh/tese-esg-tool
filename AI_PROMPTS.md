# AI Prompts Used

This document lists the AI tools and prompts used during the development of this project, as requested in the assignment.

## Development Tool

**Claude Code** (Anthropic's CLI for Claude) was used to assist with code development, architecture decisions, and implementation.

## Key Prompts Used

### 1. Project Architecture Prompt
> "Build a simple AI-powered tool that takes a company's basic sustainability data (e.g., carbon emissions, energy usage, water consumption) as input and generates a short ESG risk summary using an LLM API."

This was the original assignment prompt. Claude Code was used to research Tese.io's mission (climate adaptation + SME finance matching) and design the tool to produce finance-ready insights rather than generic scores.

### 2. ESG Analysis System Prompt (used in `esg_analyzer.py`)
The system prompt instructs Gemini to act as an ESG analyst and includes:
- Industry-specific benchmarks for comparison
- Instructions to produce finance-ready risk assessments
- Structured JSON output format with environmental risks, social/governance considerations, recommendations, and financing opportunities

See the full prompt in [`esg_analyzer.py`](esg_analyzer.py) — `SYSTEM_PROMPT` and `USER_PROMPT_TEMPLATE` variables.

### 3. Domain Research
Claude Code was used to research:
- Appropriate ESG input metrics for SME sustainability assessment
- Realistic industry benchmarks (technology, manufacturing, retail, energy, agriculture)
- Tese.io's specific focus on ISO 14090-aligned Climate Adaptation Plans and CAP-to-Finance matching

## What Was AI-Assisted vs. Human-Decided

| Aspect | Source |
|--------|--------|
| Tool architecture (CLI + Streamlit) | Human decision |
| LLM choice (Gemini 2.5 Flash) | Human decision |
| Finance-ready framing for Tese.io | AI-researched, human-approved |
| Industry benchmark data | AI-researched from public sources |
| Code implementation | AI-assisted with human review |
| Prompt engineering | Collaborative (iterative refinement) |
