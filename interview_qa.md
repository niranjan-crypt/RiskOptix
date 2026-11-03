# RiskOptix: Product Management Deep-Dive & Interview Guide
**Author & Product Architect:** Niranjan Krishnakumar  
**Domain:** Quantitative Derivatives & Trading Infrastructure  
**Product Showcase:** RiskOptix Engine  

---

## 1. Core Interview Questions & Strategic Model Answers

### Q1: Why did you choose this problem over others? (Evidence from interviews)
**Answer:**  
"When researching retail options trading in India, the most glaring problem isn’t a lack of tools—it’s **workflow fragmentation and execution anxiety**. In my discovery interviews with 7 active F&O traders, 6 of them were using Sensibull or Opstra on desktop to build strategies, but executing on Zerodha Kite or Dhan mobile. 

The moment they switch to the broker’s basket ticket, the entire aggregate risk picture disappears. 5 of 7 traders specifically cited getting burned by silent slippage on market orders because brokers only show Last Traded Price (LTP), hiding 15%–30% bid-ask spreads on OTM hedging wings. Even worse, 4 of 7 had experienced exchange leg rejections (from freeze limits or margin spikes) that left them holding naked short positions. 

I chose this problem because it addresses a major structural gap in modern trading: **execution transparency for multi-leg derivative traders**. Fixing pre-trade visibility solves an asymmetric risk that can wipe out a trader's account in minutes."

---

### Q2: What would you cut from the MVP and why?
**Answer:**  
"If engineering capacity or latency constraints forced cuts to the MVP, I would cut in this strict order:
1. **Beginner Mode overlay:** Active options traders already understand basic terminology; beginner tooltips are an onboarding enhancement rather than an execution requirement.
2. **The T-0 theoretical Greek curve:** While positional sellers appreciate seeing today's Black-Scholes curve, the primary solvency risk at confirmation is the expiry payoff step-function and max loss floor.
3. **The standalone Greeks panel (Vega, Gamma):** Net Delta and Theta are helpful, but the core financial commitment is defined by Net Debit/Credit, Max Loss, and Breakevens.

**What I would NEVER cut:**  
I would never cut **Max Loss prominently displayed (R2)**, the **Bid-Ask Spread Fill-Risk warning (R4)**, or the **Hedge-First ordering guarantee (R5)**. Without those three, the feature degenerates back into an ordinary order ticket and fails to protect the trader."

---

### Q3: Which metric would you pick as the North Star, and what could go wrong with it?
**Answer:**  
"My North Star metric is **Previewed-Price Fill Rate (PPFR)**—the percentage of multi-leg basket orders where the executed net price is within a tight tolerance ($\le 1.5$ index points) of the previewed net price.

**What could go wrong with it (The Gaming / Distortion Risk):**  
If our execution router optimizes solely for matching the previewed price, it might artificially widen the previewed spread or artificially reject orders that would experience minor, acceptable slippage. Alternatively, in fast-trending markets, an order might sit unfilled because the router is waiting for the exact previewed price, causing the trader to miss the entire market move. 

That is why PPFR must be paired with two critical guardrails:
1. **Order Confirmation Latency & Fill Latency (< 150ms)**: Ensuring orders are not artificially delayed.
2. **Order Drop-off / Cancellation Rate**: Ensuring we aren't scaring users away from valid trades through overly conservative warnings."

---

### Q4: How would you handle a leg rejection, and what are the trade-offs?
**Answer:**  
"An exchange leg rejection is the single most dangerous failure state in multi-leg trading. We evaluated three architectural approaches:
1. **Cancel All Remaining Legs:** Predictable, but if the short leg filled first, cancelling remaining orders leaves the trader holding a naked short position.
2. **Immediate Market Retry:** Preserves the strategy, but in a crashing market, retrying at market can lead to catastrophic slippage.
3. **Sequenced Hedge-First Ordering (Our Recommended Choice):** The order router fires the long protective hedging legs first. Only after the exchange acknowledges the fill are the short selling legs submitted. If the long leg is rejected, the short leg is never submitted.

**Trade-off:** Hedge-first execution adds approximately 80–120ms to total basket fill time because it requires sequential ACKs. However, in options trading, solvency always trumps sub-second latency. A trader will tolerate an 80ms delay to guarantee they are never left with naked downside exposure."

---

### Q5: What did the users say during usability testing that surprised you?
**Answer:**  
"Two things surprised me:
First, **the danger of numeric placeholders**. In prototype v1, when an unhedged strategy (like a Short Straddle) had infinite downside, the system displayed a large negative number like `-₹999,999`. Two of the five participants looked at it and said: *'Okay, so my max loss is about 10 Lakhs.'* They assumed it was a computed ceiling! That was a terrifying realization. In v2, I immediately replaced numbers with an explicit, high-visibility **`UNLIMITED RISK`** glowing crimson banner.

Second, **traders cared more about slippage in ₹ than in percentages**. When I showed *'Spread: 4.2%'*, traders hesitated. But when the prototype converted that into *'Worst-Case Slippage: ₹380'*, they instantly understood whether the trade was worth taking."

---

### Q6: How would you work with engineering on latency and compliance on disclosures?
**Answer:**  
- **With Engineering:** Pre-trade previews cannot add perceptible delay. We established a strict **150ms calculation budget**. To achieve this, the analytical engine vectorizes payoff grids in NumPy, caches Black-Scholes normal CDF tables in memory, and evaluates the preview client-side using WebSocket ticks rather than firing expensive round-trip API calls to the server.
- **With Compliance & Legal:** SEBI has strict regulations regarding margin representations and investment advice. I worked within two clear guardrails:
  1. *Explicitly disclaiming advisory:* The tool is strictly descriptive of consequences, never prescriptive (no 'Buy' or 'Sell' advice).
  2. *Labeling margin as indicative:* Because exchange SPAN margins fluctuate dynamically with portfolio offsets, our tool explicitly labels margin numbers as an *'Approximate estimate only—final requirement calculated by NSE SPAN'*, while providing an input field for the trader's official broker figure."

---

### Q7: What is wrong with your margin estimate, and how would you fix it in production?
**Answer:**  
"Our prototype uses a **defined-risk spread approximation** (Max Loss + small buffer) for hedged strategies, and a contract percentage (~11.5%) for naked options. 

**What is wrong with it:** Real exchange margin is determined by the **NSE SPAN (Standard Portfolio Analysis of Risk)** system. SPAN evaluates 16 different market simulation scenarios (varying spot price and volatility) and incorporates complex portfolio-level delta offsets across existing open positions in the trader's account. Our prototype cannot replicate the exact real-time SPAN file without exchange feeds.

**How to fix it in production:** In an institutional production environment, we query the broker's real-time risk engine directly via internal RPC before rendering the preview card, passing the active basket to fetch the broker's exact SPAN + Exposure requirement in real time."

---

## 2. Rehearsal Pitches

### The 2-Minute Elevator Pitch
> *"Hi, I'm Niranjan. I built and validated RiskOptix, an institutional-grade pre-trade risk engine for multi-leg options trading. 
> 
> In Indian retail F&O, multi-leg trading has exploded, but the execution experience is broken. In my discovery research with 7 active options traders, 71% reported suffering severe slippage on market baskets, and over half had experienced exchange leg rejections that turned defined-risk spreads into dangerous naked positions. Traders are forced to jump between Sensibull to see payoffs and Zerodha Kite to execute—and on Kite, the aggregate risk context disappears into four disconnected rows.
> 
> To solve this, I designed RiskOptix: a 6-screen pre-trade engine that shows Net Cash Flow, puts Max Loss in bold 2.6rem typography, calculates real-time worst-case bid-ask slippage, and introduces sequenced hedge-first ordering to eliminate leg rejection accidents.
> 
> I built a working Python/Streamlit prototype powered by Black-Scholes Greeks, vectorized payoffs, and a synthetic 21-strike NIFTY option chain. When I usability-tested this prototype against a standard broker order ticket across 5 traders, comprehension time for max loss plummeted from 24.4 seconds down to 4.2 seconds—an 83% speedup—while trader decision confidence surged by 109%.
> 
> Finally, I established an institutional metrics framework around a North Star of Previewed-Price Fill Rate and sub-150ms latency guardrails. This project demonstrates how thoughtful quantitative product design can eliminate execution anxiety and protect trader capital."*
