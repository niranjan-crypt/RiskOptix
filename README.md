# ⚡ RiskOptix: Pre-Trade Multi-Leg Options Risk Engine

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Prototype-FF4B4B.svg?logo=streamlit&logoColor=white)](http://localhost:8501)
[![Tests](https://img.shields.io/badge/Tests-15%20Passed%20(100%25)-success.svg)](multileg-preview/tests/)
[![Domain](https://img.shields.io/badge/Domain-Quantitative%20FinTech%20%26%20Derivatives-blueviolet.svg)](case_study.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **A pre-trade risk preview for multi-leg options orders that displays net cash flow, max profit and loss in bold typography, breakevens, margin requirements, and real-time execution fill-risk before the trader confirms.**

---

## 🎯 Why This Project?

Multi-leg index options strategies (such as Iron Condors, Straddles, and Vertical Spreads) represent the fastest-growing segment of Indian derivative retail volumes. However, retail execution workflows remain dangerously disjointed. Traders design strategies on third-party visualizers like Sensibull, but must submit orders on broker terminals (such as Zerodha Kite) where aggregate risk visibility abruptly disappears into disconnected rows of limit orders.

This project delivers an end-to-end institutional Product Management package—including **user discovery, competitor benchmarking, 2-page PRD, working Python/Streamlit prototype, usability testing, and telemetry plan**—specifically engineered to eliminate execution anxiety and silent slippage in derivative trading.

---

## 🧭 Repository Navigation

| Deliverable | File Link | Description |
| :--- | :--- | :--- |
| **Comprehensive PM Case Study** | [📄 `case_study.md`](case_study.md) | 1,500-word portfolio case study ready for portfolio link or PDF export |
| **Quantified Resume Bullets** | [📝 `resume_bullets.md`](resume_bullets.md) | High-impact XYZ-format resume bullets backed by verified usability data |
| **Interview Preparation Guide** | [🎙️ `interview_qa.md`](interview_qa.md) | In-depth answers to 7 core PM interview questions + 2-minute elevator pitch |
| **2-Page Institutional PRD** | [📋 `docs/PRD.md`](docs/PRD.md) | Detailed requirements (R1–R6), personas, leg-failure decision matrix, and constraints |
| **UX & Screen Flow Breakdown** | [🎨 `docs/wireframes_and_flow.md`](docs/wireframes_and_flow.md) | Wireframe architecture and interaction design across all 6 core screens |
| **Product Telemetry & Metrics** | [📊 `docs/metrics_plan.md`](docs/metrics_plan.md) | Funnel events, Previewed-Price Fill Rate (North Star), latency guardrails (<150ms) |
| **Plain-English Explainer** | [💡 `docs/explainer_post.md`](docs/explainer_post.md) | 500-word educational guide: *"How to read a multi-leg payoff diagram"* |
| **Trader Discovery Synthesis** | [🔍 `research/interview_synthesis.md`](research/interview_synthesis.md) | Synthesis of 7 trader interviews, pattern counts, and H1–H4 scorecard |
| **Interview Capture Matrix** | [📊 `research/interview_capture_sheet.csv`](research/interview_capture_sheet.csv) | Raw interview notes matrix across 7 active F&O traders |
| **Competitor Teardown** | [🥊 `research/competitor_benchmark.md`](research/competitor_benchmark.md) | 9-criteria side-by-side comparison: Zerodha Kite vs Sensibull vs RiskOptix |
| **Usability Testing Report** | [🧪 `research/usability_test_report.md`](research/usability_test_report.md) | 5 trader usability sessions, time-to-answer metrics (4.2s vs 24.4s control), v1 $\to$ v2 fixes |

---

## 🏗️ System Architecture & Screen Flow

```text
  +-------------------------------------------------------------------------+
  | [Screen 1] STRATEGY BUILDER                                              |
  | - Presets: Iron Condor, Bull Call Spread, Bear Put Spread, Straddle...  |
  | - Dynamic Option Chain Strike Table with Real-Time Bid/Ask              |
  | - Lot Size / Quantity Stepper (1 Lot = 25 Qty)                          |
  +-------------------------------------------------------------------------+
                                      │
                                      ▼
  +-------------------------------------------------------------------------+
  | [Screen 2] MAIN RISK PREVIEW HERO                                       |
  | ┌───────────────────────┐ ┌──────────────────┐ ┌──────────────────────┐  |
  | │ MAX LOSS: ₹3,998      │ │ MAX PROFIT: +1,002│ │ NET CREDIT: +₹1,002 │  |
  | │ (Or UNLIMITED Alert)  │ │ Breakevens: 24160│ │ Expected Slippage   │  |
  | └───────────────────────┘ └──────────────────┘ └──────────────────────┘  |
  | - Interactive Plotly Chart: Expiry Step-Payoff vs T-0 Today Curve       |
  | - Net Greeks (Delta, Gamma, Theta decay, Vega)                          |
  +-------------------------------------------------------------------------+
                                      │
              ┌───────────────────────┴───────────────────────┐
              │ (If spread > 3.5%)                            │ (If liquid)
              ▼                                               ▼
  +────────────────────────────────────+   +────────────────────────────────────+
  | [Screen 3] WARNING STATE           |   | [Screen 4] CONFIRMATION TICKET     |
  | - Crimson border on illiquid leg   |   | - One-line commitment summary:     |
  | - Spread %: 18.2%                  |   |   "Committing to Net Credit ₹1,002 |
  | - Worst-case slippage impact in ₹  |   |    with Max Loss ₹3,998"           |
  | - Limit order recommendation       |   | - [Confirm & Send] [Cancel]        |
  +────────────────────────────────────+   +────────────────────────────────────+
                                      │
                                      ▼
                      ┌─────────────────────────────────┐
                      │ (If exchange rejects a leg)     │
                      ▼                                 ▼
  +─────────────────────────────────────────────────────────────────────────+
  | [Screen 5] LEG-FAILURE RECOVERY ENGINE                                  |
  | - Banner: "Exchange Rejected Leg 4 (Buy 24900 CE)! Unhedged position"   |
  | - Visualized Red Exposed Payoff Curve                                   |
  | - 3 Direct Actions:                                                     |
  |   [Cancel All Remaining]  [Market Retry Leg]  [Hedge-First Re-route]     |
  +─────────────────────────────────────────────────────────────────────────+
                                      │
                                      ▼
  +─────────────────────────────────────────────────────────────────────────+
  | [Screen 6] BEGINNER MODE (Overlay / Toggle)                             |
  | - Plain-English context: "What is Net Debit?", "Why spreads slip"       |
  +─────────────────────────────────────────────────────────────────────────+
```

---

## 🥊 Competitor Benchmark (At a Glance)

| Criterion | Zerodha Kite (Baskets) | Sensibull | RiskOptix Engine |
| :--- | :---: | :---: | :---: |
| Clicks to Build Iron Condor | 11–14 clicks | 3–4 clicks | **2 clicks (Preset Builder)** |
| Net Cash Flow Shown Before Confirm | ❌ No | ✅ Yes | **✅ Clear Debit/Credit Badge** |
| Max Loss Before Confirm | ❌ No | ✅ Yes | **✅ 2.6rem Bold Typography** |
| Unbounded Risk Warning | ❌ No | ⚠️ Small text | **🚨 Glowing `UNLIMITED` Alert** |
| Per-Leg Bid-Ask Spread & Slippage | ❌ No | ❌ No | **✅ Real-Time Worst-Case Price** |
| Leg-Failure Recovery Mechanism | ❌ Fails silently | ❌ Delegates | **✅ 3-Way Recovery Engine** |
| Dual Payoff Chart (Expiry + T-0) | ❌ None | ✅ Web view | **✅ Integrated Plotly Engine** |

---

## 📊 Usability & Business Impact

During testing across **5 active options traders** comparing the prototype against a standard broker basket ticket:
- **Comprehension Speed:** Time to identify Max Loss fell from **24.4s** on the control ticket to **4.2s** on RiskOptix (**83% speedup**).
- **Decision Confidence:** Trader self-rated confidence rose from **2.2 / 5 to 4.6 / 5** (**+109% surge**).
- **Execution Safeguard:** Introduced **Sequenced Hedge-First Routing**, guaranteeing that protective buy legs execute before short selling legs to completely prevent unhedged naked position disasters.

---

## ⚡ Quickstart: Running Locally

### 1. Clone the Repository
```bash
git clone https://github.com/niranjan-crypt/RiskOptix.git
cd RiskOptix
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python3 -m venv multileg-preview/venv
source multileg-preview/venv/bin/activate
pip install -r multileg-preview/requirements.txt
```

### 3. Run Automated Unit Tests
```bash
pytest multileg-preview/tests/ -v
```
*Validates hand-calculated financial benchmarks (Bull Call Spread, Short Straddle, Iron Condor) and Black-Scholes Greeks.*

### 4. Launch the Interactive Web Application
```bash
streamlit run multileg-preview/app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 👨‍💻 Author & Contact

**Niranjan Krishnakumar**  
- **Email:** [niranjankrishnakumar2005@gmail.com](mailto:niranjankrishnakumar2005@gmail.com)  
- **GitHub:** [@niranjan-crypt](https://github.com/niranjan-crypt)  
- **Focus:** Quantitative Trading Systems & FinTech Product Architecture
