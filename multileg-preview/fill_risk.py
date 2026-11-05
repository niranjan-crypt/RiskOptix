"""
fill_risk.py - Execution Fill-Risk and Worst-Case Price Engine
Part of RiskOptix Quantitative Engine
"""

from typing import List, Dict, Any, Tuple


def calculate_leg_fill_risk(
    bid: float,
    ask: float,
    mid: float = None,
    volume: int = None
) -> Dict[str, Any]:
    """
    Computes fill risk for a single option leg.
    Spread % = (Ask - Bid) / Mid * 100%
    """
    if mid is None or mid <= 0:
        mid = (bid + ask) / 2.0 if (bid + ask) > 0 else 1.0

    spread_pts = max(ask - bid, 0.0)
    spread_pct = (spread_pts / mid) * 100.0 if mid > 0 else 0.0

    # Risk level thresholding
    if spread_pct < 1.5 and (volume is None or volume > 100000):
        risk_level = "LOW"
        risk_color = "#10B981"  # Emerald green
        description = "Liquid strike. Tight spread; low slippage expected."
    elif spread_pct <= 3.5 and (volume is None or volume > 30000):
        risk_level = "MODERATE"
        risk_color = "#F59E0B"  # Amber
        description = "Moderate spread. Market order may experience slight slippage."
    else:
        risk_level = "HIGH"
        risk_color = "#EF4444"  # Rose / red
        description = "Wide spread or thin liquidity! Limit orders strongly recommended."

    return {
        "bid": round(bid, 2),
        "ask": round(ask, 2),
        "mid": round(mid, 2),
        "spread_pts": round(spread_pts, 2),
        "spread_pct": round(spread_pct, 2),
        "risk_level": risk_level,
        "risk_color": risk_color,
        "description": description,
    }


def calculate_strategy_execution_risk(
    legs: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes overall strategy execution risk:
    - Expected Net Price (at Mid)
    - Worst-Case Net Price (Buy at Ask, Sell at Bid)
    - Maximum Slippage Exposure (₹ and %)
    - Flagged illiquid or high-risk legs
    """
    total_mid_cashflow = 0.0
    total_worst_cashflow = 0.0
    leg_assessments = []
    has_high_risk_leg = False

    for idx, leg in enumerate(legs):
        side = leg["side"]  # +1 buy, -1 sell
        lots = leg.get("lots", 1)
        lot_size = leg.get("lot_size", 25)
        qty = lots * lot_size

        bid = leg.get("bid", leg.get("premium", 0.0))
        ask = leg.get("ask", leg.get("premium", 0.0))
        mid = leg.get("mid", leg.get("premium", (bid + ask) / 2.0))
        volume = leg.get("volume", None)

        leg_eval = calculate_leg_fill_risk(bid=bid, ask=ask, mid=mid, volume=volume)
        leg_eval["leg_index"] = idx + 1
        leg_eval["strike"] = leg.get("strike")
        leg_eval["type"] = leg.get("type")
        leg_eval["side_str"] = "BUY" if side == 1 else "SELL"

        if leg_eval["risk_level"] == "HIGH":
            has_high_risk_leg = True

        # Expected cashflow at Mid
        total_mid_cashflow += -side * mid * qty

        # Worst-case cashflow: Buy at Ask, Sell at Bid
        exec_price = ask if side == 1 else bid
        leg_eval["worst_exec_price"] = exec_price
        total_worst_cashflow += -side * exec_price * qty

        leg_assessments.append(leg_eval)

    # Slippage is the difference between expected and worst-case
    slippage_loss = abs(total_worst_cashflow - total_mid_cashflow)

    return {
        "expected_net_cashflow": round(total_mid_cashflow, 2),
        "worst_net_cashflow": round(total_worst_cashflow, 2),
        "slippage_exposure_inr": round(slippage_loss, 2),
        "has_high_risk_leg": has_high_risk_leg,
        "legs": leg_assessments
    }
