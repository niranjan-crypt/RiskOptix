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
    assert pytest.approx(max_l, 1e-1) == -2000.0

    # 4. Breakeven
    bes = find_breakevens(spot_grid, payoffs)
    assert len(bes) == 1, f"Expected 1 breakeven, got {len(bes)}"
    assert pytest.approx(bes[0], abs=1.0) == 24580.0


def test_short_straddle_unlimited_risk():
    """
    Short Straddle:
    Sell 24500 CE @ 125, Sell 24500 PE @ 120. Lot size = 25, 1 lot.
    - Net Credit = (125 + 120) * 25 = +6,125 INR
    - Max Profit = +6,125 INR at spot 24500
    - Max Loss = UNLIMITED on both sides!
    - Breakevens: 24500 - 245 = 24255 and 24500 + 245 = 24745
    """
    legs = [
        {"side": -1, "type": "CE", "strike": 24500.0, "premium": 125.0, "lots": 1, "lot_size": 25},
        {"side": -1, "type": "PE", "strike": 24500.0, "premium": 120.0, "lots": 1, "lot_size": 25},
    ]

    net_cf = calculate_net_premium(legs)
    assert net_cf == 6125.0, f"Expected net credit +6125.0, got {net_cf}"

    spot_grid = np.linspace(20000, 29000, 9001)
    payoffs = calculate_strategy_payoff(spot_grid, legs)

    max_p, inf_p, max_l, inf_l = calculate_max_profit_loss(spot_grid, payoffs)
    assert not inf_p, "Short straddle profit is capped at collected premium"
    assert inf_l, "Short straddle must flag UNLIMITED loss"
    assert pytest.approx(max_p, 1e-1) == 6125.0

    bes = find_breakevens(spot_grid, payoffs)
    assert len(bes) == 2, f"Expected 2 breakevens, got {len(bes)}"
    assert pytest.approx(bes[0], abs=1.0) == 24255.0
    assert pytest.approx(bes[1], abs=1.0) == 24745.0


def test_iron_condor_defined_risk():
    """
    4-Leg Iron Condor:
    Buy 24000 PE @ 13.0, Sell 24200 PE @ 32.0, Sell 24700 CE @ 25.1, Buy 24900 CE @ 4.0
    Lot size = 25, 1 lot.
    - Net premium collected = (-13.0 + 32.0 + 25.1 - 4.0) * 25 = 40.1 * 25 = +1,002.50 INR
    - Put spread width = 200 pts, Call spread width = 200 pts
    - Max loss = (200 - 40.1) * 25 = 159.9 * 25 = -3,997.50 INR
    - Both wings hedged -> Defined risk (not unlimited)
    """
    legs = [
        {"side": 1, "type": "PE", "strike": 24000.0, "premium": 13.0, "lots": 1, "lot_size": 25},
        {"side": -1, "type": "PE", "strike": 24200.0, "premium": 32.0, "lots": 1, "lot_size": 25},
        {"side": -1, "type": "CE", "strike": 24700.0, "premium": 25.1, "lots": 1, "lot_size": 25},
        {"side": 1, "type": "CE", "strike": 24900.0, "premium": 4.0, "lots": 1, "lot_size": 25},
    ]

    net_cf = calculate_net_premium(legs)
    assert pytest.approx(net_cf, 0.1) == 1002.50

    spot_grid = np.linspace(22000, 27000, 5001)
    payoffs = calculate_strategy_payoff(spot_grid, legs)

    max_p, inf_p, max_l, inf_l = calculate_max_profit_loss(spot_grid, payoffs)
    assert not inf_p, "Iron Condor profit must be bounded"
    assert not inf_l, "Iron Condor loss must be bounded"
    assert pytest.approx(max_p, 1e-1) == 1002.50
    assert pytest.approx(max_l, 1e-1) == -3997.50

    bes = find_breakevens(spot_grid, payoffs)
    assert len(bes) == 2, f"Expected 2 breakevens for Iron Condor, got {bes}"
    # Lower BE = 24200 - 40.1 = 24159.9
    # Upper BE = 24700 + 40.1 = 24740.1
    assert pytest.approx(bes[0], abs=1.0) == 24159.9
    assert pytest.approx(bes[1], abs=1.0) == 24740.1
