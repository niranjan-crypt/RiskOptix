"""
payoff.py - Strategy Payoff, Breakevens, and Max Profit/Loss Calculations
Part of RiskOptix Quantitative Engine
"""

from typing import List, Dict, Any, Tuple
import numpy as np


def calculate_net_premium(legs: List[Dict[str, Any]]) -> float:
    """
    Computes the net premium cash flow for the strategy.
    Rule: sum of (-side * premium * lots * lot_size)
    - Negative return indicates a Net Debit (trader pays cash upfront).
    - Positive return indicates a Net Credit (trader collects cash upfront).
    """
    net_cash_flow = 0.0
    for leg in legs:
        side = leg["side"]  # +1 for Buy, -1 for Sell
        premium = leg["premium"]
        lots = leg.get("lots", 1)
        lot_size = leg.get("lot_size", 25)
        net_cash_flow += -side * premium * lots * lot_size
    return net_cash_flow


