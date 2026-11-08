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
│   ├── order_ticket.py         # Pre-trade commitment confirmation ticket
│   └── failure_recovery.py     # Execution anomaly and 3-tier recovery engine
├── data/
│   └── nifty_options_chain.csv # 21-strike synthetic NIFTY 50 options chain snapshot
├── tests/
│   ├── test_payoff.py          # Unit tests verifying payoff math & breakevens
│   ├── test_greeks.py          # Unit tests for Black-Scholes Greeks & T-0 decay
│   ├── test_fill_risk.py       # Unit tests for bid-ask spread & slippage
│   ├── test_margin.py          # Unit tests for defined-risk SPAN calculations
│   └── test_models.py          # Unit tests for domain models & serialization
└── requirements.txt            # Python dependencies
```

---

## Key Features

1. **Strategy Builder (Screen 1):** Pre-configured multi-leg strategies (Iron Condor, Bull Call Spread, Bear Put Spread, Short Straddle, Long Strangle, or Custom up to 4 legs).
2. **Main Risk Preview (Screen 2):**
   - **Hero Max Loss Card:** Displays worst-case loss in large 2.6rem bold typography. Highlights unbounded naked positions with an animated `UNLIMITED RISK` crimson badge.
   - **Net Cash Flow:** Clear distinction between Net Debit (cash paid upfront) and Net Credit (cash collected upfront).
   - **Breakevens:** Exact zero-crossing spot prices computed via linear interpolation.
3. **Dynamic Payoff Chart:** Dual-line Plotly visualization rendering both the Friday **Expiry Payoff Curve** and the theoretical **T-0 Payoff Curve (Today)** with Black-Scholes time decay.
4. **Fill-Risk & Slippage Panel (Screen 3):** Analyzes per-leg bid-ask spread % ($\frac{\text{Ask} - \text{Bid}}{\text{Mid}} \times 100\%$) and calculates the exact worst-case execution cash flow (Buy @ Ask, Sell @ Bid) to quantify market impact.
5. **Margin Requirements:** Compares user's broker calculator SPAN figure against max loss, with defined-risk hedge savings calculation.
6. **Leg-Failure Anomaly Simulator (Screen 5):** Toggle exchange rejection on outer protective legs to visualize unhedged exposure and test 3 recovery strategies: Cancel All, Market Retry, and Sequenced Hedge-First Routing.
7. **Beginner Mode (Screen 6):** Top-bar toggle providing plain-English explanations beside all financial metrics.
8. **Headless CLI:** Run options risk evaluations directly from the terminal via `python cli.py --preset condor`.

---

## Local Setup & Quickstart

### 1. Run Automated Unit Tests
```bash
pytest tests/ -v
```

### 2. Run Headless CLI Evaluator
```bash
python cli.py --preset condor --lots 2
```

### 3. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501` to interact with the application.
