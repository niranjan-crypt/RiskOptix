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


def calculate_max_profit_loss(
    spot_grid: np.ndarray,
    payoff_grid: np.ndarray
) -> Tuple[float, bool, float, bool]:
    """
    Determines max profit, max loss, and checks if payoff is unbounded ('Unlimited').
    
    Returns:
        (max_profit, is_profit_unlimited, max_loss, is_loss_unlimited)
        Note: max_loss is returned as an absolute negative amount (or float('-inf')).
    """
    raw_max = float(np.max(payoff_grid))
    raw_min = float(np.min(payoff_grid))

    # Evaluate slopes at the boundaries to detect open-ended unbounded risk
    left_slope = (payoff_grid[1] - payoff_grid[0]) / (spot_grid[1] - spot_grid[0])
    right_slope = (payoff_grid[-1] - payoff_grid[-2]) / (spot_grid[-1] - spot_grid[-2])

    slope_threshold = 0.05  # Any sustained slope indicates unbounded trajectory

    is_profit_unlimited = False
    is_loss_unlimited = False

    # Left edge (spot -> 0)
    if left_slope < -slope_threshold:
        # As spot decreases, payoff increases (e.g., naked put buy or short call)
        is_profit_unlimited = True
    elif left_slope > slope_threshold:
        # As spot decreases, payoff plunges (e.g., short put)
        is_loss_unlimited = True

    # Right edge (spot -> infinity)
    if right_slope > slope_threshold:
        # As spot increases, payoff increases (e.g., naked call buy)
        is_profit_unlimited = True
    elif right_slope < -slope_threshold:
        # As spot increases, payoff plunges into catastrophic loss (e.g., short call)
        is_loss_unlimited = True

    max_profit = float("inf") if is_profit_unlimited else raw_max
    max_loss = float("-inf") if is_loss_unlimited else raw_min

    return max_profit, is_profit_unlimited, max_loss, is_loss_unlimited


def find_breakevens(
    spot_grid: np.ndarray,
    payoff_grid: np.ndarray
) -> List[float]:
    """
    Finds spot prices where the strategy payoff crosses 0 (break-even points)
    using exact linear interpolation between adjacent grid points.
    """
    breakevens = []
    for i in range(len(spot_grid) - 1):
        y1, y2 = payoff_grid[i], payoff_grid[i + 1]
        x1, x2 = spot_grid[i], spot_grid[i + 1]

        # Check for zero crossing
        if y1 == 0:
            breakevens.append(round(float(x1), 2))
        elif (y1 < 0 and y2 > 0) or (y1 > 0 and y2 < 0):
            # Linear interpolation: x = x1 - y1 * (x2 - x1) / (y2 - y1)
            x_cross = x1 - y1 * (x2 - x1) / (y2 - y1)
            breakevens.append(round(float(x_cross), 2))

    # Remove duplicates close to each other
    unique_bes = []
    for be in breakevens:
        if not any(abs(be - u) < 1.0 for u in unique_bes):
            unique_bes.append(be)

    return sorted(unique_bes)
