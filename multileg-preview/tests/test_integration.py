"""
test_integration.py - End-to-End Pipeline Integration Test
"""

import numpy as np
import pytest
from payoff import (
    calculate_net_premium,
    calculate_strategy_payoff,
    calculate_max_profit_loss,
    find_breakevens,
)
from greeks import calculate_strategy_greeks, calculate_today_payoff
from fill_risk import calculate_strategy_execution_risk
from margin import calculate_defined_risk_margin_estimate, format_broker_margin_comparison
from models import OptionLeg, PayoffResult


def test_full_iron_condor_pipeline():
    """Validates complete multi-leg execution workflow for a standard 4-leg Iron Condor."""
    spot = 24500.0
    lot_size = 25
    lots = 2
    t_years = 3 / 365.0

    legs = [
        {"side": 1, "type": "PE", "strike": 24100, "bid": 19, "ask": 21, "mid": 20, "premium": 20, "lots": lots, "lot_size": lot_size},
        {"side": -1, "type": "PE", "strike": 24300, "bid": 48, "ask": 51, "mid": 49.5, "premium": 49.5, "lots": lots, "lot_size": lot_size},
        {"side": -1, "type": "CE", "strike": 24700, "bid": 54, "ask": 56, "mid": 55, "premium": 55, "lots": lots, "lot_size": lot_size},
        {"side": 1, "type": "CE", "strike": 24900, "bid": 9, "ask": 10, "mid": 9.5, "premium": 9.5, "lots": lots, "lot_size": lot_size},
    ]

    # 1. Payoff Math
    spot_grid = np.linspace(spot * 0.85, spot * 1.15, 601)
    payoffs_expiry = calculate_strategy_payoff(spot_grid, legs)
    max_p, is_p_unlim, max_l, is_l_unlim = calculate_max_profit_loss(spot_grid, payoffs_expiry)
    bes = find_breakevens(spot_grid, payoffs_expiry)
    net_premium = calculate_net_premium(legs)

    assert not is_p_unlim
    assert not is_l_unlim
    assert max_p > 0
    assert max_l < 0
    assert len(bes) == 2
    assert net_premium > 0  # Net credit collected

    # 2. Greeks & Today Payoff
    greeks = calculate_strategy_greeks(spot, legs, time_to_expiry_years=t_years)
    payoffs_today = calculate_today_payoff(spot_grid, legs, time_to_expiry_years=t_years)
    assert len(payoffs_today) == len(spot_grid)
    assert greeks["net_theta"] > 0  # Condor benefits from theta decay

    # 3. Execution Risk & Slippage
    exec_risk = calculate_strategy_execution_risk(legs)
    assert exec_risk["slippage_exposure_inr"] >= 0
    assert len(exec_risk["legs"]) == 4

    # 4. Margin Requirements
    margin = calculate_defined_risk_margin_estimate(legs, max_l, is_l_unlim, spot)
    assert margin["estimated_margin_inr"] > 0
    assert margin["hedge_benefit_inr"] > 0

    # 5. Broker Margin Comparison
    comp = format_broker_margin_comparison(75000.0, max_l, is_l_unlim)
    assert "capital_at_risk_ratio" in comp
