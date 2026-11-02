# Product Requirements Document (PRD)
## RiskOptix — Pre-Trade Options Risk & Execution Engine
**Document Version:** 2.0 (Post-Usability Iteration)  
**Author:** Niranjan Krishnakumar (Product Management & Architecture)  
**Product:** RiskOptix Platform  
**Target Release:** Production Ready  

---

## 1. Executive Summary
Traders placing multi-leg options strategies currently execute blind to aggregated portfolio outcomes, suffering unexpected worst-case slippage, margin spikes, and unhedged leg rejections. This feature introduces **RiskOptix**—an institutional-grade, pre-trade risk preview dialog embedded directly into the multi-leg order ticket for index options. Before committing capital, traders gain instant visibility into their true maximum loss, net cash flow, breakevens, worst-case execution price, and automated contingency protections.

---

## 2. Background & Evidence
- **Interview Findings:** In our discovery research with 7 active F&O traders, 71% (5/7) reported experiencing severe execution slippage on multi-leg market orders, 57% (4/7) suffered account crises when a hedging leg was rejected by exchange filters, and 86% (6/7) currently toggle between external charting tools (Sensibull) and broker tickets due to fragmented UX.
- **Incumbent Gaps:** Competitor teardowns of Zerodha Kite and Sensibull reveal that Kite offers zero pre-trade payoff feedback in its basket ticket, while Sensibull calculates theoretical values assuming frictionless mid-market fills with zero bid-ask spread warnings or leg-rejection safety netting.

---

## 3. Users & Use Cases

### Persona 1: Vikram — The Expiry-Day Scalper
- **Profile:** 29, trades 0DTE NIFTY and BANKNIFTY short straddles and spreads during weekly expiries. Submits 10–20 lots.
- **Core Need:** Millisecond latency and immediate visibility into bid-ask slippage. Needs to know if illiquid OTM wings will cause catastrophic execution cost before submitting market baskets.

### Persona 2: Ananya — The Positional Options Seller
- **Profile:** 34, software engineer deploying 4-leg Iron Condors and Iron Butterflies for consistent theta decay, holding across multiple days.
- **Core Need:** Capital efficiency and risk capping. Needs to guarantee that her max loss is strictly bounded, understand her exact margin requirement, and view theoretical P&L today (T-0) vs expiry.

### Scenario 3: The Transitioning Beginner
- **Profile:** Retail trader transitioning from naked call buying to defined-risk spreads to avoid account drawdowns.
- **Core Need:** Confidence and clarity. Needs clear distinction between net debit (cash leaving account) and net credit, with plain-English terminology explaining risk.

---

## 4. Goals & Non-Goals

### **Goals:**
- Provide a sub-150ms aggregated risk preview before order dispatch.
- Eliminate trader uncertainty regarding worst-case financial commitment.
- Safeguard traders against unhedged naked exposure caused by partial fills or exchange leg rejections.

### **Non-Goals (Out of Scope):**
- **Automated Trading / Execution Bots:** The preview engine does not execute automated trades.
- **Equity Cash or Crypto Assets:** Confined strictly to Indian index options (NIFTY, BANKNIFTY, FINNIFTY).
- **Trade Advisory / Recommendation:** The tool displays the exact mathematical consequences of the trader's chosen strategy; it does *not* provide buy/sell recommendations or financial advice.

---

## 5. Functional Requirements

