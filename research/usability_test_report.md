# Phase 6: Usability Testing & Iteration Report
**Project:** RiskOptix — Options Risk Engine Prototype  
**Cohort:** 5 Active Options Traders (2 Expiry Scalpers, 2 Positional Sellers, 1 Beginner)  
**Methodology:** 20-minute moderated think-aloud usability sessions over screen-share evaluating prototype v1 against a standard control order ticket (Zerodha basket format).  
**Lead Researcher:** Niranjan Krishnakumar  

---

## 1. Usability Metrics & Quantitative Results

| Participant ID | Trader Archetype | Task 1: Comprehend Max Loss (Preview) | Task 1: Time to Answer (Preview vs Control) | Confidence Rating (Before $\to$ After Preview) | Task 2: Spot Illiquid Leg (Fill Risk) | Task 3: Leg Rejection Response |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **P1** | Positional Seller (3y) | **Yes (100%)** | **3.8s** (vs 24.5s Control) | $2 / 5 \to 5 / 5$ | Spotted 24900 CE (Spread 18%) | Clicked "Hedge-First Recovery" |
| **P2** | Expiry Scalper (4y) | **Yes (100%)** | **3.1s** (vs 19.2s Control) | $3 / 5 \to 5 / 5$ | Spotted 24100 PE immediately | Clicked "Cancel All Remaining" |
| **P3** | Newer Trader (8m) | **Yes (100%)** | **5.4s** (vs Failed Control) | $1 / 5 \to 4 / 5$ | Needed Beginner Mode toggle | Clicked "Hedge-First Recovery" |
| **P4** | Positional Seller (2y) | **Yes (100%)** | **4.2s** (vs 31.0s Control) | $2 / 5 \to 4 / 5$ | Spotted high spread warning badge | Requested automated retry |
| **P5** | Expiry Scalper (1.5y) | **Yes (100%)** | **4.5s** (vs 22.8s Control) | $3 / 5 \to 5 / 5$ | Spotted illiquid OTM wing | Clicked "Cancel All Remaining" |
| **Average / Summary** | — | **5 / 5 (100%)** | **4.2 seconds** (vs **24.4s** on Control) | **$2.2 \to 4.6$ (+109% increase)** | **5 / 5 identified** | **Unanimous relief at recovery options** |

---

## 2. Qualitative Feedback & Participant Quotes

> *"On the standard ticket, I spent nearly 30 seconds scanning through limit prices, trying to remember if 24100 was the buy leg or the sell leg to calculate my spread width. On the RiskOptix preview, the red ₹3,998 card hits you right in the face in 3 seconds. There is zero ambiguity."*  
> — **P1 (Positional Seller)**

> *"The worst-case execution slippage card is genius. In expiry afternoons, brokers show you mid-price, but you get filled 15 points worse. Showing that ₹160 worst-case slippage beforehand tells me immediately whether I should switch to limit orders."*  
> — **P2 (Expiry Scalper)**

> *"When I first started trading Iron Condors, I lived in fear of one leg being rejected and blowing up my account. Seeing the 3 contingency recovery buttons right under the failure state makes me feel protected."*  
> — **P3 (Newer Trader)**

---

## 3. Issues Identified & Severity Triage

| Issue ID | Severity | Observation / Friction Point | Root Cause |
| :--- | :--- | :--- | :--- |
| **ISSUE-01** | **BLOCKER** | When a strategy had unbounded risk (Short Straddle), the numeric field displayed `-₹999,999` which misled 2 users into thinking their risk was capped at 10 Lakhs. | Numeric placeholder was used instead of an explicit visual categorical state. |
| **ISSUE-02** | **MAJOR** | Traders wanted to see the theoretical P&L *today* (T-0 curve), not just expiry payoff, because positional sellers often exit at 50% max profit before expiry. | Initial prototype only rendered the Friday expiry step-function curve. |
| **ISSUE-03** | **MAJOR** | Margin required was initially shown as an exact number without explanation, confusing users whose brokers showed slightly different SPAN figures. | Lack of clear distinction between broker SPAN inputs and defined-risk estimates. |
| **ISSUE-04** | **MINOR** | Newer traders were intimidated by Greek symbols ($\Delta, \Gamma, \Theta, \nu$) without contextual translation into ₹ values. | Technical jargon lacked plain-language financial descriptors. |

---

## 4. Prototype Iteration: What Was Changed (v1 $\to$ v2)

1. **Resolution of ISSUE-01 (Blocker):**  
   Replaced numeric overflow values with a dedicated high-priority **`UNLIMITED RISK` hero card** featuring a distinct glowing crimson border and descriptive warning text: *"Strategy carries unbounded risk! Can trigger full liquidation."*
2. **Resolution of ISSUE-02 (Major):**  
   Integrated Black-Scholes analytical pricer into the Plotly graph to render a **dashed gold T-0 curve** side-by-side with the solid blue expiry curve, allowing traders to see their expected P&L today.
3. **Resolution of ISSUE-03 (Major):**  
   Split margin into **Option A** (Broker SPAN user input with capital-at-risk ratio) and **Option B** (Hedged defined-risk estimator), explicitly watermarked with the disclaimer: *"Approximate estimate only; exchange SPAN calculated by broker."*
4. **Resolution of ISSUE-04 (Minor):**  
   Added a top-level **"Beginner Mode" toggle** that automatically injects plain-language explanations beside Greeks (e.g. *"Theta: ₹28.50/day money earned from time decay"*).
