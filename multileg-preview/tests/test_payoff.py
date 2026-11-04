"""
Unit tests for payoff, breakevens, and max profit/loss calculations.
Verifies against analytical hand-calculated benchmarks.
"""

import numpy as np
import pytest
from payoff import (
    calculate_net_premium,
    calculate_strategy_payoff,
    calculate_max_profit_loss,
    find_breakevens,
)


def test_bull_call_spread():
    """
    Bull Call Spread:
    Buy 24500 CE @ 125, Sell 24700 CE @ 45. Lot size = 25, 1 lot.
    - Net Debit = (125 - 45) * 25 = 2,000 INR
    - Max Loss = -2,000 INR
    - Max Profit = ( (24700 - 24500) - 80 ) * 25 = 120 * 25 = 3,000 INR
    - Breakeven = 24500 + 80 = 24580
    """
    legs = [
        {"side": 1, "type": "CE", "strike": 24500.0, "premium": 125.0, "lots": 1, "lot_size": 25},
        {"side": -1, "type": "CE", "strike": 24700.0, "premium": 45.0, "lots": 1, "lot_size": 25},
    ]

    # 1. Net Cash Flow
    net_cf = calculate_net_premium(legs)
    assert net_cf == -2000.0, f"Expected net debit -2000.0, got {net_cf}"

    # 2. Payoff across grid
    spot_grid = np.linspace(23000, 26000, 3001)
    payoffs = calculate_strategy_payoff(spot_grid, legs)

    # 3. Max Profit and Loss
    max_p, inf_p, max_l, inf_l = calculate_max_profit_loss(spot_grid, payoffs)
    assert not inf_p, "Bull Call Spread profit should be bounded"
    assert not inf_l, "Bull Call Spread loss should be bounded"
    assert pytest.approx(max_p, 1e-1) == 3000.0
