# Phase 2: Competitor Benchmark Teardown
**Task Benchmark:** Configure and review a 4-leg Iron Condor on NIFTY 50 (nearest weekly expiry) up to the final confirmation step.  
**Platforms Benchmarked:** Zerodha Kite, Sensibull, RiskOptix Architecture  
**Evaluator:** Niranjan Krishnakumar  

---

## 1. Feature Comparison Matrix

| Evaluation Criterion | Zerodha Kite (Baskets) | Sensibull (Strategy Builder) | RiskOptix Engine |
| :--- | :--- | :--- | :--- |
| **1. Taps/Clicks to build 4-leg Iron Condor** | **11–14 clicks** (Search strike $\to$ select strike $\to$ select CE/PE $\to$ set buy/sell $\to$ add to basket $\times 4$) | **3–4 clicks** (Pick NIFTY $\to$ select 'Iron Condor' preset $\to$ adjust strikes on slider) | **2 clicks** (Select preset $\to$ select lots; automatic strike populator from chain) |
| **2. Order Dispatch Format** | Basket execution (orders fired simultaneously as single API batch) | Fired via Broker Basket API (or virtual paper trade) | Atomic Multi-Leg Order with sequenced hedge-first routing |
| **3. Net Premium shown before confirm** | **No** (Shows individual leg limits/market prices only; requires mental math) | **Yes** (Clear net credit / debit indicator in ₹ and points) | **Yes** (Explicit Net Debit/Credit badge with cash flow direction) |
| **4. Max Profit & Max Loss shown before confirm** | **No** (Order ticket shows no payoff metrics whatsoever) | **Yes** (Detailed max profit, max loss, and reward-to-risk ratio) | **Yes** (Hero Max Loss card with animated `UNLIMITED` risk alert for naked legs) |
| **5. Breakeven Points shown** | **No** | **Yes** (Shows lower and upper breakeven spot prices) | **Yes** (Interactive breakeven vertical markers on payoff curve) |
| **6. Margin shown before confirm** | **Yes** (Shows 'Required Margin' and 'Final Margin' with hedge discount) | **Yes** (Calculates theoretical SPAN + Exposure) | **Yes** (Displays broker margin input comparison + defined-risk hedge savings) |
| **7. Fill-Risk or Bid-Ask Spread Warning** | **No** (Shows LTP only; no warning if order book spread is 15% wide) | **No** (Payoff calculation assumes mid-price fills without liquidity warnings) | **Yes** (Computes per-leg spread %, flags illiquid strikes, calculates worst-case fill) |
| **8. Behavior if One Leg is Rejected** | **Fails silently / Leaves partial positions naked** (Remaining orders execute regardless) | N/A (Delegates execution to underlying broker; no recovery state) | **Yes** (Interactive Leg-Failure Engine: prompts Cancel All, Market Retry, or Hedge-First) |
| **9. Interactive Payoff Chart Available in Flow** | **No** (Must open third-party tool) | **Yes** (Interactive desktop chart with T-0 curve) | **Yes** (Integrated Plotly chart with T-0 curve, expiry curve, and spot markers) |

---

## 2. Where the Gaps Are (Strategic PM Synthesis)

### **Gap 1: The "Execution Disconnect" between Analysis and Confirmation**
Traders experience a disjointed handoff between analytical platforms and broker execution engines. While Sensibull offers superior payoff visualization, order execution is handed over to broker webviews or raw basket tickets where critical risk context (Max Loss, Breakevens, Greeks) completely disappears. A trader making a last-second decision on Zerodha Kite is looking at raw limit prices with zero aggregate risk feedback.

### **Gap 2: The "Mid-Price Illusion" and Slippage Neglect**
Both Kite and Sensibull evaluate strategies assuming instantaneous execution at mid-market prices or Last Traded Price (LTP). In actual market conditions (especially near weekly expiries or on OTM protection wings), wide bid-ask spreads cause slippage of 5–15 points per leg. Neither competitor alerts the trader to order book depth or displays a **Worst-Case Net Price** (buying at ask, selling at bid).

### **Gap 3: Complete Absence of Leg-Failure Safeguards**
The most catastrophic UX failure in Indian multi-leg trading occurs when an exchange rejects one leg (e.g. hitting SEBI freeze limits or price execution bands) while executing the other three. In Zerodha Kite, this silently turns a defined-risk Iron Condor into an unhedged, naked short position, prompting immediate margin shortfall penalties and panic. Neither incumbent provides an automated contingency state or pre-trade hedge-first guarantee.

### **The RiskOptix Strategic Advantage:**
By combining rapid strategy presets with a pre-trade preview showing **Max Loss in bold typography, Worst-Case Slippage alerts, and Leg-Failure contingency routing**, RiskOptix solves the exact anxiety points where incumbents abandon the trader.
