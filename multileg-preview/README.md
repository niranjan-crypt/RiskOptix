# RiskOptix — Interactive Multi-Leg Options Risk Engine

An institutional-grade pre-trade options risk and execution engine built with Python, Streamlit, NumPy, SciPy, and Plotly.

---

## Architecture Overview

```text
multileg-preview/
├── app.py                      # Streamlit Application Orchestrator
├── cli.py                      # Headless CLI Strategy Evaluation Tool
├── config.py                   # Centralized Configuration & Parameters
├── models.py                   # Strongly-Typed Domain Dataclasses
├── payoff.py                   # Vectorized payoff math, breakevens, max P/L
├── greeks.py                   # Black-Scholes analytical engine, Greeks, T-0 curve
├── fill_risk.py                # Bid-ask spread % analysis and worst-case price simulator
├── margin.py                   # Defined-risk vs broker SPAN margin calculator helper
├── components/                 # Modular Streamlit UI Components
│   ├── styles.py               # Dark fintech theme and CSS injection
│   ├── sidebar.py              # Strategy configurator and leg builders
│   ├── hero_metrics.py         # Max Loss hero card and top KPIs
│   ├── payoff_chart.py         # Interactive Plotly multi-curve payoff graph
│   ├── slippage_panel.py       # Fill-risk table and slippage alerts
│   ├── greeks_margin.py        # Portfolio Greeks and SPAN margin panel
