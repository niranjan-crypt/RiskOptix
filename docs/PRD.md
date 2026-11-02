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

| Req ID | Requirement Description | Acceptance Criteria |
| :--- | :--- | :--- |
| **R1** | **Net Strategy Cash Flow** | Display net debit (cash paid upfront) or net credit (cash received) in ₹ and points across all legs. Color-coded (Emerald for credit, Sky-blue for debit). |
| **R2** | **Max Profit, Max Loss & Breakevens** | Show worst-case loss in bold 2.6rem typography. If any leg is unhedged (e.g. short call/put), display prominent `UNLIMITED RISK` badge. Calculate exact zero-crossing breakeven spot prices via linear interpolation. |
| **R3** | **Margin & Hedge Benefit** | Allow user input of broker SPAN figure (Option A) and compute defined-risk estimate (Option B). Explicitly display hedge discount and mandatory disclaimer: *"Estimate only; broker SPAN rules apply."* |
| **R4** | **Per-Leg Fill Risk & Worst-Case Price** | Calculate spread %: $\frac{\text{Ask} - \text{Bid}}{\text{Mid}} \times 100\%$. Flag illiquid strikes ($>3.5\%$ spread). Compute worst-case net execution price (Buy at Ask, Sell at Bid) and total ₹ slippage. |
| **R5** | **Leg-Failure Contingency Engine** | If an exchange rejects one or more legs, display an emergency state presenting 3 recovery options: Cancel All, Market Retry, or Hedge-First re-routing. |
| **R6** | **Dual Payoff Visualization** | Render an interactive chart displaying both Expiry Payoff (step-function) and Today's T-0 Theoretical Curve (Black-Scholes), with current spot price and breakeven indicators. |

---

## 6. Leg-Failure Handling: Options Decision Table

When an order router encounters a partial fill or exchange leg rejection, the platform must handle the unhedged legs. Below is the comparative trade-off analysis:

| Strategy | Pros | Cons | Decision Rationale |
| :--- | :--- | :--- | :--- |
| **Option 1: Cancel All Remaining Legs** | Simple, immediate, stops further capital allocation. | Leaves already-filled legs unhedged in the market, exposing the trader to severe directional tail risk. | Rejected as standalone default; acceptable only as a manual fallback. |
| **Option 2: Immediate Market Retry** | Preserves intended spread structure and hedge. | In fast-moving markets, retrying at market can lead to severe slippage or repeated rejections. | High risk in volatile conditions; useful only with price-band limits. |
| **Option 3: Sequenced Hedge-First Ordering (Recommended)** | **Guarantees trader protection:** Long hedging wings are executed and confirmed *before* short legs are fired. Eliminates naked margin spikes. | Increases total basket dispatch latency by ~80–120ms. | **RECOMMENDED & ADOPTED:** In options trading, preventing catastrophic unlimited risk takes precedence over 100ms latency. |

**Final Architectural Recommendation:**  
Adopt **Sequenced Hedge-First Ordering** as the default submission architecture. If an exchange rejects the protective long leg, the short leg is never submitted, ensuring the user's capital is never left naked.

---

## 7. Edge Cases & Handling Rules
1. **SEBI Freeze Quantity Limits:** If order quantity exceeds exchange freeze limits (e.g. 1,800 qty for NIFTY), the engine automatically splits orders into compliant slices before computing fill risk.
2. **Illiquid Deep OTM Strikes:** Strikes with bid-ask spread $>10\%$ or zero open orders display a prominent warning dialog requiring explicit user acknowledgment.
3. **Execution Near Market Close (3:20 PM IST):** Intraday MIS orders trigger an auto-square-off warning highlighting the risk of broker RMS liquidation.
4. **Exchange Execution Price Bands:** Out-of-band limit orders are validated locally before submission to prevent exchange-level order rejection.

---

## 8. Constraints & Compliance
- **Latency Budget:** Total calculation time for payoff, Greeks, and fill risk must complete in $<150\text{ms}$ on standard mobile/web clients.
- **SEBI Regulatory Compliance:** Mandatory regulatory disclaimer displayed on all preview cards: *"Educational risk simulation; not investment advice. Margin figures are indicative."* (To confirm with Legal & Compliance team).

---

## 9. Feature Prioritization & MVP Cut Line

| Req ID | Feature Area | User Impact | Engineering Effort | Release Scope |
| :--- | :--- | :---: | :---: | :--- |
| **R1** | Net Debit / Credit Display | High | Low | **MVP (Phase 1)** |
| **R2** | Max Profit, Max Loss & Breakevens | Critical | Medium | **MVP (Phase 1)** |
| **R4** | Bid-Ask Spread & Worst-Case Slippage | High | Medium | **MVP (Phase 1)** |
| **R6** | Expiry & T-0 Payoff Chart | High | Medium | **MVP (Phase 1)** |
| **R3** | Margin Calculator & Broker SPAN Comparison | High | Low | **MVP (Phase 1)** |
| **R5** | Leg-Failure Recovery Engine | Critical | High | **v1.1 (Follow-on Release)** |
| — | Beginner Mode Plain-English Explanations | Medium | Low | **v1.1 (Follow-on Release)** |

*(MVP Cut Line established at R1, R2, R4, R6, and R3).*
