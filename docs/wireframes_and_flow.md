# Phase 4: UI/UX Wireframe Specifications & User Flow
**Document:** RiskOptix — Multi-Leg Options Risk Engine Screen Flow Architecture  
**Author:** Niranjan Krishnakumar  

---

## 1. Core Design Principles
1. **Consequences Before Actions:** Never allow an order confirmation before displaying the worst-case monetary outcome.
2. **The "One Number" Rule:** Max Loss is the most critical solvency metric for an options trader; it must always be rendered in the largest typography on screen (2.6rem).
3. **Zero Hidden Defaults:** No default lot size or strike selection without explicit visual feedback.
4. **Honest Estimation Labeling:** All margin figures and theoretical Greeks must be clearly watermarked as mathematical estimates.

---

## 2. Screen-by-Screen Layouts & Specifications

```
  +-------------------------------------------------------------------------+
  | [Screen 1] STRATEGY BUILDER                                              |
  | - Strategy Preset Selector (Iron Condor, Bull Call Spread, Straddle...) |
  | - Lot Size / Quantity Stepper (1 Lot = 25 Qty)                          |
  | - Dynamic Option Chain Strike Table with Real-Time Bid/Ask              |
  +-------------------------------------------------------------------------+
                                      |
                                      v
  +-------------------------------------------------------------------------+
  | [Screen 2] MAIN RISK PREVIEW CARD                                       |
  | +-----------------------+ +------------------+ +----------------------+  |
  | | MAX LOSS: ₹3,998      | | MAX PROFIT: +1,002| | NET CREDIT: +₹1,002 |  |
  | | (Or UNLIMITED Alert)  | | Breakevens: 24160| | Expected Slippage   |  |
  | +-----------------------+ +------------------+ +----------------------+  |
  | - Interactive Plotly Chart: Expiry Step-Payoff vs T-0 Today Curve       |
  | - Net Greeks (Delta, Gamma, Theta decay, Vega)                          |
  +-------------------------------------------------------------------------+
                                      |
              +-----------------------+-----------------------+
              | (If spread > 3.5%)                            | (If liquid)
              v                                               v
  +------------------------------------+   +------------------------------------+
  | [Screen 3] WARNING STATE           |   | [Screen 4] CONFIRMATION TICKET     |
  | - Crimson border alert on illiquid |   | - One-line commitment summary:     |
  |   strike (e.g. 24900 CE OTM wing)  |   |   "Committing to Net Credit ₹1,002 |
  | - Spread %: 18.2%                  |   |    with Max Loss ₹3,998"           |
  | - Slippage penalty quantified in ₹ |   | - [Confirm & Send] [Cancel]        |
  +------------------------------------+   +------------------------------------+
                                      |
                                      v
                      +---------------------------------+
                      | (If exchange rejects a leg)     |
                      v                                 v
  +-------------------------------------------------------------------------+
  | [Screen 5] LEG-FAILURE RECOVERY ENGINE                                  |
  | - Banner: "Exchange Rejected Leg 4 (Buy 24900 CE)! Unhedged position"   |
  | - Visualized Red Exposed Payoff Curve                                   |
  | - 3 Direct Actions:                                                     |
  |   [Cancel All Remaining]  [Market Retry Leg]  [Hedge-First Re-route]     |
  +-------------------------------------------------------------------------+
                                      |
                                      v
  +-------------------------------------------------------------------------+
  | [Screen 6] BEGINNER MODE (Overlay / Toggle)                             |
  | - Contextual tooltip cards explaining every financial concept:          |
  |   "What is a Net Debit?", "Why does Bid-Ask Spread cause slippage?",    |
  |   "How Theta decay earns money while you sleep"                         |
  +-------------------------------------------------------------------------+
```

---

## 3. UI Component Details

### Screen 1: Strategy Builder
- **Inputs:** Dropdown preset list with pre-calculated strike combinations (Iron Condor, Bull Call Spread, Bear Put Spread, Short Straddle, Long Strangle) or custom builder up to 4 legs.
- **Controls:** Lot size numeric stepper (1 to 100 lots), auto-multiplying lot size by NSE contract lot size (25).

### Screen 2: Risk Preview (Main Hero Screen)
- **Hero Card (Max Loss):**
  - Bounded Loss: `#1E1114` dark red card with `#EF4444` border, showing `-₹X,XXX`.
  - Unbounded Loss: `#450A0A` glowing card with flashing crimson border and bold `UNLIMITED RISK` text.
- **Supporting Stats:** Max Profit, Net Cash Flow (Sky-blue for debit, Emerald for credit), Breakeven points.
- **Dual Payoff Visualization:** Plotly interactive line graph with T-0 curve (dashed gold) and Expiry curve (cyan), featuring hover tooltips at every strike.

### Screen 3: Warning State (Fill Risk)
- **Illiquid Leg Card:** Amber/Rose alert highlighting any strike with spread $>3.5\%$.
- **Worst-Case Net Price:** Explicit comparison: Expected Mid Cash Flow vs Worst-Case Execution Cash Flow (Buy @ Ask, Sell @ Bid).

### Screen 4: Confirmation Screen
- **One-Line Commitment Summary:** Clean plain-English text:  
  *"You are committing to: Net Credit of ₹1,002. Your absolute maximum risk is ₹3,998. Required margin is ₹14,200."*
- **Primary Action CTA:** Emerald `Confirm & Send Basket` button with micro-interaction state.

### Screen 5: Leg-Failure Emergency State
- **Anomaly Banner:** Appears if order router reports an error on any individual leg.
- **Decision Engine Actions:** Three distinct buttons with pros and cons clearly enumerated.

### Screen 6: Beginner Mode
- **Toggle:** Located in top navigation bar. When enabled, adds educational contextual callouts explaining options terminology without cluttering the screen for pro traders.
