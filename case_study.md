# Case Study: RiskOptix — Eliminating Silent Slippage & Margin Accidents in Multi-Leg Options Trading
**Product Architect & Lead PM:** Niranjan Krishnakumar  
**Domain:** Quantitative Derivatives & FinTech Systems  
**Project Scope:** Discovery, Benchmarking, PRD, Mathematical Prototype & Usability Testing  
**Live Prototype:** Streamlit App in `multileg-preview/`  

---

## 1. Executive Summary
Multi-leg index options strategies (such as Iron Condors, Straddles, and Vertical Spreads) represent the fastest-growing segment of Indian derivative retail volumes. However, retail execution workflows remain dangerously disjointed. Traders design strategies on third-party visualizers like Sensibull, but must submit orders on broker terminals (such as Zerodha Kite) where aggregate risk visibility abruptly disappears into disconnected rows of limit orders. 

This product initiative conceptualizes, designs, and validates **RiskOptix**—an institutional-grade pre-trade options risk engine that aggregates net cash flow, highlights maximum loss in prominent typography, calculates real-time worst-case execution slippage across order book spreads, and provides automated contingency protection against leg rejections.

Through discovery interviews with 7 active F&O traders, competitor benchmarking against Kite and Sensibull, an analytical Python/Streamlit prototype, and usability testing across 5 traders, this project demonstrates how pre-trade transparency reduced time-to-comprehend max loss from **24.4s to 4.2s** and elevated trader execution confidence by **109%**.

---

## 2. Research & Discovery (The Problem Behind the Trades)

### Research Methodology
To anchor product decisions in real trading behaviors rather than assumptions, I interviewed **7 active F&O traders** across three archetypes:
- **Intraday & Expiry Scalpers (2):** Trading 0DTE NIFTY contracts with 10–20 lots, hyper-sensitive to slippage.
- **Positional Options Sellers (3):** Deploying multi-day defined-risk spreads (Iron Condors, Butterflies).
- **Newer Options Traders (2):** Retail traders with $<1$ year experience transitioning from naked buying to hedged spreads.

### Core Discoveries & Hypothesis Validation
1. **The "Mid-Price Slippage Trap" (H2 Validated, 71% Prevalence):** 5 of 7 traders reported severe financial slippage on market basket orders. Broker tickets display Last Traded Price (LTP), hiding that outer protective wings often suffer 15%–30% bid-ask spreads.
2. **The "Leg-Rejection Margin Shock" (H4 Validated, 57% Prevalence):** 4 of 7 traders experienced catastrophic margin spikes when an exchange rejected a single hedging leg (due to freeze limits or price execution bands), converting their safe defined-risk spread into an unhedged naked position.
3. **Severe Workflow Fragmentation (H3 Validated, 86% Prevalence):** 6 of 7 traders maintained two or more screens—building on Sensibull or Opstra, but executing on Kite or Dhan—introducing cognitive delay and manual input errors.

---

## 3. Competitor Benchmarking & Gap Analysis

I conducted a standardized task benchmark: **Building and reviewing a 4-leg Iron Condor on NIFTY up to the confirmation step across Zerodha Kite, Sensibull, and RiskOptix**.

| Feature / Capability | Zerodha Kite (Baskets) | Sensibull | RiskOptix Engine |
| :--- | :---: | :---: | :---: |
| Taps to Configure 4-Leg Strategy | 11–14 clicks | 3–4 clicks | **2 clicks (Preset Builder)** |
| Pre-Trade Net Cash Flow (Debit/Credit) | ❌ Not Shown | ✅ Shown | **✅ Prominent Color-Coded Badge** |
| Max Profit & Max Loss Visibility | ❌ Not Shown | ✅ Shown (Desktop) | **✅ Hero Typography (2.6rem)** |
| Unlimited Risk Alert for Naked Legs | ❌ Not Shown | ⚠️ Small text | **🚨 Glowing Crimson Alert State** |
| Per-Leg Bid-Ask Spread / Slippage Warning | ❌ Not Shown | ❌ Not Shown | **✅ Real-Time Worst-Case Price** |
| Leg-Failure Recovery Mechanism | ❌ Fails silently | ❌ Delegates to broker | **✅ 3-Way Contingency Engine** |
| Integrated Dual Payoff Chart (Expiry + T-0) | ❌ None | ✅ Web view | **✅ Integrated Plotly Engine** |

**The Strategic Opportunity:** RiskOptix eliminates the gap between *analytical modeling* and *broker order dispatch*. By embedding real-time solvency and slippage calculations directly into the pre-trade flow, RiskOptix eliminates execution anxiety.

---

## 4. Product Definition & Technical Architecture

### Core Product Requirements
- **R1: Net Cash Flow:** Clear distinction between Net Debit (cash leaving account) and Net Credit (cash collected upfront).
- **R2: Hero Solvency Metric (Max Loss):** Designed around the principle: *"Show one number that matters most in the largest type."* If risk is open-ended, the engine flags `UNLIMITED RISK`.
- **R3: Fill-Risk & Slippage Quantifier:** Evaluates each leg's spread $\frac{\text{Ask} - \text{Bid}}{\text{Mid}} \times 100\%$. Computes worst-case net execution (buying at ask, selling at bid) to show traders their absolute slippage exposure in ₹ before confirmation.
- **R4: Dual Payoff Visualization:** Renders both the step-function Expiry Curve and the smooth Black-Scholes T-0 Curve (payoff today), enabling positional traders to plan early profit-taking.
- **R5: Leg-Failure Decision Architecture:** Rather than leaving traders stranded when exchange filters reject a leg, RiskOptix provides three actionable pathways: Cancel All, Market Retry, or Hedge-First re-routing.

### Architectural Decision: Sequenced Hedge-First Ordering
In the PRD decision table, I evaluated three architectural options for handling basket execution:
1. *Concurrent Dispatch:* Fast but leaves partial fills naked.
2. *Cancel-All Fallback:* Leaves already-filled legs unhedged.
3. *Sequenced Hedge-First Routing (Recommended):* The execution engine dispatches outer protective buy legs first. Only upon receiving exchange ACK are the short selling legs fired. If the protective leg is rejected, the short leg is never submitted. While adding ~80–120ms to total basket dispatch, it mathematically guarantees that an account is never left naked.

---

## 5. Prototype Implementation

To prove technical viability, I engineered a fully functioning Python application (`multileg-preview/`):
- **Option Chain Data Layer:** Realistic synthetic snapshot of NIFTY 50 weekly options across 21 strike levels with volatility smile (IV 13%–16%) and realistic bid-ask depth.
- **Mathematical Payoff Engine (`payoff.py`):** Vectorized evaluation across 600 spot price points, exact linear interpolation for breakeven detection, and boundary-slope verification to identify unbounded risk.
- **Black-Scholes & Greeks Engine (`greeks.py`):** Closed-form formulas for Delta, Gamma, Theta decay, Vega, and theoretical T-0 pricing across the spot grid.
- **Interactive UI (`app.py`):** Streamlit interface built with RiskOptix's dark fintech design language, interactive Plotly charts, live fill-risk badges, and a simulated leg-rejection toggle.
- **Verification:** 100% test coverage across 6 automated unit tests validating hand-calculated financial benchmarks (Bull Call Spread, Short Straddle, Iron Condor).

---

## 6. Usability Testing & Iterative Design

I conducted moderated usability sessions with **5 active options traders** comparing the RiskOptix Prototype against a standard broker basket ticket.

### Quantitative Results
- **Time to Comprehend Max Loss:** Decreased by **83%** (from an average of **24.4 seconds** on the control ticket to **4.2 seconds** on RiskOptix).
- **Trader Confidence Score:** Rose from **2.2 / 5 to 4.6 / 5** (+109% increase) before and after reviewing the preview.
- **Identification of Illiquid Legs:** 5 of 5 traders immediately spotted wide-spread strikes using the fill-risk warning panel.

### Critical Iterations from User Feedback (v1 $\to$ v2)
1. **The "Numeric Overflow" Trap (Blocker):** In v1, unbounded risk was displayed as `-₹999,999`, which misled two traders into thinking their risk was capped at ₹10 Lakhs. In v2, I replaced this with an explicit **`UNLIMITED RISK`** glowing crimson banner.
2. **Missing T-0 Curve (Major):** Positional sellers requested the theoretical curve *today* because they rarely hold to 3:30 PM expiry. I integrated Black-Scholes today-payoff modeling into the Plotly chart.
3. **Beginner Accessibility (Minor):** Added a top-bar **"Beginner Mode"** toggle providing plain-English explanations for complex options terms without cluttering pro workflows.

---

## 7. Metrics & Instrumentation Framework

### Primary Metric (North Star): Previewed-Price Fill Rate (PPFR)
- **Definition:** Percentage of multi-leg basket orders where the executed net price matches the previewed net price within a tolerance band of $\le 1.5$ index points.
- **Target:** $\ge 92\%$ across all standard market sessions.

### Secondary Metrics
- **Median Time to Confirm:** Target $\le 6.5$ seconds (ensuring risk transparency accelerates rather than hinders execution).
- **Preview Engagement Rate:** Target $\ge 88\%$ opt-in adoption.

### Guardrail Metrics
- **Order Placement Latency:** Server-side preview calculation must stay strictly below **150ms** at p95.
- **Leg Rejection Rate:** Must not rise above baseline ($3.2\%$).
- **Customer Support Tickets:** Margin shortfall disputes and fill complaints should fall by $\ge 30\%$ within two months of launch.

---

## 8. What I Would Do Next (Product Roadmap)
1. **Smart Order Routing (SOR) with Dynamic Slicing:** Integrate automated order slicing when order volume exceeds exchange freeze limits (e.g. 1,800 contracts on NIFTY).
2. **Implied Volatility (IV) Stress Slider:** Allow traders to interactively slide IV up or down ($\pm 5\%$) on the preview screen to visualize Greek sensitivity during high-impact macro announcements (RBI policy, budget days).
3. **Post-Trade Leg Management:** Extend the pre-trade preview framework into post-trade position management, alerting traders when widening spreads on existing positions threaten square-off thresholds.
