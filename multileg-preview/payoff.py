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


def calculate_leg_payoff_expiry(
    spot: np.ndarray,
    side: int,
    opt_type: str,
    strike: float,
    premium: float,
    lots: int = 1,
    lot_size: int = 25
) -> np.ndarray:
    """
    Calculates the payoff for a single leg at expiry across a grid of spot prices.
    Payoff = side * lots * lot_size * (intrinsic - premium)
    """
    opt_type = opt_type.upper()
    if opt_type in ("CE", "CALL"):
        intrinsic = np.maximum(spot - strike, 0.0)
    elif opt_type in ("PE", "PUT"):
        intrinsic = np.maximum(strike - spot, 0.0)
    else:
        raise ValueError(f"Unknown option type: {opt_type}. Must be 'CE' or 'PE'.")

    return side * lots * lot_size * (intrinsic - premium)


def calculate_strategy_payoff(
    spot_grid: np.ndarray,
    legs: List[Dict[str, Any]]
) -> np.ndarray:
    """
    Evaluates the combined payoff of all strategy legs at expiry.
    """
    total_payoff = np.zeros_like(spot_grid, dtype=float)
    for leg in legs:
        leg_payoff = calculate_leg_payoff_expiry(
            spot=spot_grid,
            side=leg["side"],
            opt_type=leg["type"],
            strike=leg["strike"],
            premium=leg["premium"],
            lots=leg.get("lots", 1),
            lot_size=leg.get("lot_size", 25)
        )
        total_payoff += leg_payoff
    return total_payoff


