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


