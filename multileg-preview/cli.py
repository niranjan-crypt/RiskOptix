"""
cli.py - Command Line Interface for Headless RiskOptix Strategy Evaluation
"""

import argparse
import json
import numpy as np
from typing import Dict, Any

from config import DEFAULT_SPOT_PRICE, DEFAULT_DAYS_TO_EXPIRY, DEFAULT_LOT_SIZE
from payoff import (
    calculate_net_premium,
    calculate_strategy_payoff,
    calculate_max_profit_loss,
    find_breakevens,
)
from greeks import calculate_strategy_greeks
from fill_risk import calculate_strategy_execution_risk
from margin import calculate_defined_risk_margin_estimate


def evaluate_preset(preset: str, lots: int = 2) -> Dict[str, Any]:
    """Evaluates a standard options preset strategy."""
    spot = DEFAULT_SPOT_PRICE
    lot_size = DEFAULT_LOT_SIZE
    t_years = DEFAULT_DAYS_TO_EXPIRY / 365.0

    if preset == "condor":
        legs = [
            {"side": 1, "type": "PE", "strike": 24100, "bid": 19, "ask": 21, "mid": 20, "premium": 20, "lots": lots, "lot_size": lot_size},
            {"side": -1, "type": "PE", "strike": 24300, "bid": 48, "ask": 51, "mid": 49.5, "premium": 49.5, "lots": lots, "lot_size": lot_size},
            {"side": -1, "type": "CE", "strike": 24700, "bid": 54, "ask": 56, "mid": 55, "premium": 55, "lots": lots, "lot_size": lot_size},
            {"side": 1, "type": "CE", "strike": 24900, "bid": 9, "ask": 10, "mid": 9.5, "premium": 9.5, "lots": lots, "lot_size": lot_size},
        ]
    elif preset == "straddle":
        legs = [
            {"side": -1, "type": "CE", "strike": 24500, "bid": 107, "ask": 109, "mid": 108, "premium": 108, "lots": lots, "lot_size": lot_size},
            {"side": -1, "type": "PE", "strike": 24500, "bid": 114, "ask": 116, "mid": 115, "premium": 115, "lots": lots, "lot_size": lot_size},
        ]
    else:  # bull call spread
        legs = [
            {"side": 1, "type": "CE", "strike": 24500, "bid": 107, "ask": 109, "mid": 108, "premium": 108, "lots": lots, "lot_size": lot_size},
            {"side": -1, "type": "CE", "strike": 24700, "bid": 54, "ask": 56, "mid": 55, "premium": 55, "lots": lots, "lot_size": lot_size},
        ]

    spot_grid = np.linspace(spot * 0.85, spot * 1.15, 601)
    payoffs = calculate_strategy_payoff(spot_grid, legs)
    max_p, is_p_unlim, max_l, is_l_unlim = calculate_max_profit_loss(spot_grid, payoffs)
    bes = find_breakevens(spot_grid, payoffs)
    net_premium = calculate_net_premium(legs)
    greeks = calculate_strategy_greeks(spot, legs, time_to_expiry_years=t_years)
    exec_risk = calculate_strategy_execution_risk(legs)
    margin = calculate_defined_risk_margin_estimate(legs, max_l, is_l_unlim, spot)

    return {
        "strategy": preset,
        "lots": lots,
        "net_premium_inr": net_premium,
        "max_profit": "UNLIMITED" if is_p_unlim else max_p,
        "max_loss": "UNLIMITED" if is_l_unlim else max_l,
        "breakevens": bes,
        "net_delta": greeks["net_delta"],
        "net_theta": greeks["net_theta"],
        "slippage_exposure_inr": exec_risk["slippage_exposure_inr"],
        "estimated_margin_inr": margin["estimated_margin_inr"],
    }


def main():
    parser = argparse.ArgumentParser(description="RiskOptix Headless Quantitative Strategy Evaluator")
    parser.add_argument("--preset", choices=["condor", "spread", "straddle"], default="condor", help="Strategy preset")
    parser.add_argument("--lots", type=int, default=2, help="Number of lots")
    args = parser.parse_args()

    results = evaluate_preset(args.preset, args.lots)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
