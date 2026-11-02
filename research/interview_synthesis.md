# Phase 1: User Research Synthesis & Hypothesis Scorecard
**Project:** RiskOptix — Multi-Leg Options Risk Engine  
**Author / PM:** Niranjan Krishnakumar  

---

## 1. Participant Cohort Overview
To understand trader workflows and execution pain points when placing multi-leg index options strategies, 7 active F&O traders were interviewed (20-minute structured semi-structured sessions):
- **2 Expiry-Day / Intraday Scalpers:** Fast-paced execution, trade high lot sizes on 0DTE NIFTY/BANKNIFTY options, sensitive to sub-second slippage.
- **3 Positional Sellers:** Deploy 2-to-4 leg defined-risk spreads (Iron Condors, Iron Butterflies, Calendar Spreads) holding overnight or across the weekly cycle.
- **2 Newer F&O Traders (<1 year experience):** Transitioned from single-leg buying to defined spreads for risk control, but struggle with order ticketing and margin requirements.

---

## 2. Emergent Patterns & Quantitative Findings

| Pattern Observed | Prevalence | Quantitative Count | Impact Level |
| :--- | :--- | :--- | :--- |
| **P1: Slippage Blindspot on Basket Orders** | Traders commit to multi-leg orders seeing only mid-market prices; they do not know what worst-case fills will cost them across wide bid-ask spreads. | **5 of 7 traders (71%)** | **High / Financial Loss** |
| **P2: Tool Fragmentation (Builder vs Execution)** | Traders use analytical tools (Sensibull, Opstra) to visualize payoffs, but must copy-paste or switch to broker order tickets (Kite, Dhan) where the aggregate risk preview vanishes. | **6 of 7 traders (86%)** | **High / Latency & Error** |
| **P3: Margin & Freeze Rejection Panic** | At least one leg fails (due to exchange freeze quantity limits, price bands, or instantaneous margin recalculations), leaving remaining legs unhedged and naked. | **4 of 7 traders (57%)** | **Critical / Unbounded Risk** |
| **P4: Confusion over Pre-Trade Net Position** | Newer and intermediate traders cannot quickly verify whether their basket is a net debit or credit before hitting 'Submit'. | **3 of 7 traders (43%)** | **Moderate / Cognitive Load** |

---

## 3. Direct Anonymized Quotes

> *"Sensibull is great for visualizing payoff graphs on desktop, but the moment I fire a basket order on Kite mobile, the final confirmation screen just lists four disconnected rows. In that split second before market open, I can't confirm my net debit or max loss. I just hold my breath and click."*  
> — **T3 (Positional Seller, 3 years exp)**

> *"During expiry afternoon volatility, I placed a 4-leg Iron Condor. The short legs got filled, but the protective OTM put was rejected on a freeze-quantity error. Kite immediately converted it into a naked short position and spiked my required margin by ₹1.4 Lakhs. I spent the next 10 minutes frantically trying to cover before my account got squared off."*  
> — **T2 (Positional Seller, BANKNIFTY)**

> *"I bought a strangle thinking each leg cost only ₹8. I didn't check the order book depth—the spread was 22% wide. The moment the market order went through, I was already down ₹1,800 on slippage alone. Nobody warned me before I confirmed."*  
> — **T4 (Newer F&O Trader, 6 months exp)**

---

## 4. Hypothesis Testing Scorecard

| Hypothesis | Predicted Behavior | Outcome | Evidence from Interviews |
| :--- | :--- | :--- | :--- |
| **H1** | Traders do not know their max loss before they confirm a multi-leg order. | **Validated (Partial)** | **4 of 7** traders could not compute or locate max loss on their broker's native order ticket. Advanced traders knew their intended theoretical loss from Sensibull, but lacked confirmation in the broker execution ticket. |
| **H2** | Traders have had at least one bad outcome from legs filling unevenly or one leg being rejected. | **Validated (Strong)** | **5 of 7** traders recounted severe losses or panic from partial fills, wide spread execution, or exchange freeze limits breaking their hedge. |
| **H3** | Traders use two or more tools (e.g. Sensibull to build, Kite to execute) because no single broker screen shows everything. | **Validated (Strong)** | **6 of 7** traders actively toggle between an analytics site (Sensibull/Opstra) and their broker app, leading to execution latency and cognitive fatigue. |
| **H4** | Margin surprises (required margin differs from expected) are a common frustration. | **Validated** | **4 of 7** traders experienced margin spikes, unexpected shortfall penalties, or blocked orders due to broker execution ordering (short leg executing before long hedge). |

---

## 5. The Single Problem Selected to Solve

### **Problem Statement:**
> **Traders executing multi-leg options strategies suffer unhedged risk, margin surprises, and silent slippage because broker confirmation tickets present disconnected leg rows rather than an aggregated pre-trade risk preview showing Net Debit/Credit, Max Loss, Breakevens, Worst-Case Slippage, and Leg-Failure Contingencies.**

### **Why this problem?**
1. **Direct Market Alignment:** Modern active traders increasingly deploy multi-leg spreads and demand transparent, institutional-grade execution safeguards. Solving multi-leg execution transparency turns order entry from a source of anxiety into a defensible competitive moat.
2. **High Severity / Asymmetric Risk:** A single rejected hedging leg can wipe out months of options selling gains. Preventing execution accidents via pre-trade warnings delivers immediate, tangible monetary value to users.
