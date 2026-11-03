# Phase 7: Product Telemetry & Metrics Plan
**Product:** RiskOptix — Multi-Leg Pre-Trade Options Risk Engine  
**Author:** Niranjan Krishnakumar  

---

## 1. Instrumentation & Event Taxonomy

Every trader interaction with the multi-leg order workflow is instrumented with structured telemetry events:

| Event Name | Trigger Point | Payload Properties |
| :--- | :--- | :--- |
| `strategy_built` | User selects or customizes a multi-leg combination. | `strategy_type`, `num_legs`, `underlying` ("NIFTY"), `lots`, `is_preset` (boolean) |
| `preview_viewed` | Pre-trade risk preview card renders. | `net_type` ("debit"/"credit"), `net_amount`, `max_loss_type` ("bounded"/"unlimited"), `max_loss_val`, `calc_latency_ms` |
| `preview_warning_shown` | Bid-ask spread $>3.5\%$ or low volume detected on $\ge 1$ leg. | `flagged_strikes` (array), `max_spread_pct`, `slippage_exposure_inr` |
| `order_confirmed` | User taps 'Confirm & Send Basket' button. | `expected_net_price`, `worst_case_net_price`, `time_to_confirm_ms` |
| `order_executed` | Exchange confirms all leg fills. | `executed_net_price`, `fill_latency_ms`, `slippage_delta_inr` |
| `leg_rejected` | Exchange order router fails to fill $\ge 1$ leg. | `failed_leg_index`, `rejection_reason` ("FREEZE_LIMIT", "MARGIN_SHORTFALL", "PRICE_BAND") |
| `recovery_action_clicked`| User selects recovery action in failure state. | `action_type` ("cancel_remaining", "market_retry", "hedge_first") |
| `order_cancelled` | User cancels order from preview dialog. | `stage_cancelled`, `time_spent_ms` |

---

## 2. Metrics Architecture (North Star, Primary, Secondary, Guardrails)

```
                            +-----------------------------------+
                            | NORTH STAR METRIC                 |
                            | Previewed-Price Fill Rate (PPFR)  |
                            | (Target: >= 92% within tolerance) |
                            +-----------------------------------+
                                              |
                     +------------------------+------------------------+
                     |                                                 |
                     v                                                 v
  +-------------------------------------+           +-------------------------------------+
  | SECONDARY METRICS                   |           | GUARDRAIL METRICS                   |
  | 1. Median Time to Confirm           |           | 1. Leg Rejection / Cancellation Rate|
  |    (Target: <= 6.5 seconds)         |           |    (Must not rise above 3.2%)       |
  | 2. Preview Engagement Rate          |           | 2. Order-Entry Latency (< 150ms)    |
  |    (Target: >= 88% adoption)        |           | 3. Margin / Fill Support Tickets    |
  |                                     |           |    (Target: >= 30% reduction)       |
  +-------------------------------------+           +-------------------------------------+
```

### **A. Primary (North Star) Metric: Previewed-Price Fill Rate (PPFR)**
- **Definition:** The percentage of multi-leg basket orders where the executed net price is within a predefined tolerance band ($\le 1.5$ index points or $\le 1.0\%$ of previewed net price).
- **Formula:**
  $$\text{PPFR} = \frac{\sum \text{Orders with } |\text{Net}_{\text{executed}} - \text{Net}_{\text{previewed}}| \le \text{Tolerance}}{\text{Total Multi-Leg Orders Executed}} \times 100\%$$
- **Business Rationale:** Directly measures whether RiskOptix delivers on its promise of execution predictability and zero slippage surprises.

### **B. Secondary Metrics**
1. **Median Time to Confirm:** Time elapsed from strategy configuration to order confirmation. Ensures the preview accelerates user decision-making rather than acting as a bureaucratic blocker.
2. **Preview Engagement Rate:** Percentage of total multi-leg orders where the trader reviewed the preview screen rather than using a bypass shortcut.

### **C. Guardrail Metrics**
1. **Basket Rejection Rate:** Must NOT increase post-launch. (If pre-trade warnings cause hesitation leading to stale orders, this metric will spike).
2. **Preview Render Latency:** Must remain $<150\text{ms}$ at p95. If Black-Scholes Greek and payoff calculations lag, active scalpers will drop off.
3. **Margin Shortfall & Fill Dispute Support Tickets:** Should decline by at least $30\%$ within 60 days of launch.

---

## 3. A/B Testing & Rollout Strategy

| Phase | Traffic Allocation | Cohort Definition | Success Criteria & Rollout Gates |
| :--- | :--- | :--- | :--- |
| **Stage 1 (Internal Beta)** | 0% Public | Internal quant team & alpha traders | Verify calculation engine accuracy across 500+ live synthetic contracts. |
| **Stage 2 (Pilot A/B Test)**| 10% Treatment / 90% Control | Random assignment among active F&O traders | Run for 14 trading sessions (2 full expiry cycles). |
| **Stage 3 (Scale Rollout)** | 50% Treatment | Broader retail F&O segment | Promote if PPFR increases by $\ge 8\%$ with zero degradation in guardrails. |
| **Stage 4 (General Avail.)**| 100% | All production user accounts | Ship to production. |

### **Automated Circuit Breaker / Rollback Rule:**
If at any point during Stage 2 or 3:
1. P95 order entry latency exceeds **250ms**, OR
2. Order drop-off / abandonment rate increases by $>5\%$ vs control, OR
3. Leg rejection rate spikes by $>1.5\times$ baseline,  
$\implies$ **The experiment automatically pauses and rolls back to standard order entry.**

---

## 4. Prototype Findings vs Production Measurements
- **What Was Measured in Prototype (Usability Test):** Task completion rate (100%), Time to comprehend max loss (4.2s vs 24.4s control), qualitative confusion points, subjective confidence ratings.
- **What Will Be Measured in Production (This Plan):** Real-world slippage vs book depth, server-side execution latency, broker SPAN margin call rates, and aggregate customer support ticket volume.
