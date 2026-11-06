"""
margin.py - Margin and Capital Requirements Calculation Helper
Part of RiskOptix Quantitative Engine
"""

from typing import Dict, List, Any


def calculate_defined_risk_margin_estimate(
    legs: List[Dict[str, Any]],
    max_loss: float,
    is_loss_unlimited: bool,
    spot_price: float = 24500.0
) -> Dict[str, Any]:
    """
    Computes an approximate defined-risk margin requirement (Option B).
    
    Disclaimer:
    Exchange margin (SPAN + Exposure) uses complex multi-scenario VAR matrices.
    This estimator provides a theoretical defined-risk baseline only.
    """
    lot_size = legs[0].get("lot_size", 25) if legs else 25
    lots = legs[0].get("lots", 1) if legs else 1

    if is_loss_unlimited:
        # Naked positions require full exchange SPAN margin (~10% to 12% of underlying contract value)
        contract_value = spot_price * lot_size * lots
        span_approx = contract_value * 0.115  # approx 11.5% for index options
        exposure_approx = contract_value * 0.02
        total_estimate = span_approx + exposure_approx
        hedge_benefit = 0.0
        margin_type = "UNBOUNDED RISK (Full SPAN + Exposure)"
        note = "Unhedged position requires full contract margin. Not eligible for spread hedge discounts."
    else:
        # Fully hedged defined-risk strategy (e.g. Iron Condor, Bull Call Spread)
        # Margin required by exchanges is generally max loss + a small buffer (~15% of spread width)
        defined_loss = abs(max_loss)
        buffer = 0.15 * defined_loss
        total_estimate = defined_loss + buffer

        # Theoretical naked margin without hedge
        unhedged_margin = spot_price * lot_size * lots * 0.135
        hedge_benefit = max(unhedged_margin - total_estimate, 0.0)
        margin_type = "DEFINED RISK (Hedged Spread)"
        note = "Eligible for exchange hedge benefit under SEBI margin framework."

    return {
        "estimated_margin_inr": round(total_estimate, 2),
        "hedge_benefit_inr": round(hedge_benefit, 2),
        "margin_type": margin_type,
        "disclaimer": "Approximate estimate only. Actual broker requirement determined by NSE SPAN.",
        "note": note
    }


def format_broker_margin_comparison(
    broker_margin_input: float,
    max_loss: float,
    is_loss_unlimited: bool
) -> Dict[str, Any]:
    """
    Option A: Formats user-provided margin directly from broker calculator,
    comparing it against strategy Max Loss and available capital.
    """
    if is_loss_unlimited:
        capital_ratio = "N/A (Unlimited Loss)"
        warning = "CRITICAL: Potential loss exceeds margin deposited!"
    else:
        defined_loss = abs(max_loss)
        if broker_margin_input > 0:
            ratio = (defined_loss / broker_margin_input) * 100.0
            capital_ratio = f"{round(ratio, 1)}%"
            warning = "Max loss is fully covered by required margin." if ratio <= 100 else "Max loss exceeds margin!"
        else:
            capital_ratio = "0.0%"
            warning = "Enter broker margin to evaluate capital efficiency."

    return {
        "broker_margin_inr": round(broker_margin_input, 2),
        "capital_at_risk_ratio": capital_ratio,
        "comparison_note": warning
    }
