"""
test_fill_risk.py - Unit Tests for Execution Fill Risk & Slippage Engine
"""

import pytest
from fill_risk import calculate_leg_fill_risk, calculate_strategy_execution_risk


def test_calculate_leg_fill_risk_liquid():
    """Test liquid strike with tight spread yields LOW risk."""
    res = calculate_leg_fill_risk(bid=100.0, ask=101.0, mid=100.5, volume=350000)
    assert res["risk_level"] == "LOW"
    assert res["spread_pts"] == 1.0
    assert res["spread_pct"] < 1.5


def test_calculate_leg_fill_risk_illiquid():
    """Test illiquid strike with wide spread yields HIGH risk."""
    res = calculate_leg_fill_risk(bid=10.0, ask=15.0, mid=12.5, volume=1000)
    assert res["risk_level"] == "HIGH"
    assert res["spread_pct"] > 3.5


def test_strategy_execution_risk_slippage():
    """Test slippage calculation across multiple legs."""
    legs = [
        {"side": 1, "type": "CE", "strike": 24500, "bid": 100, "ask": 105, "mid": 102.5, "lots": 2, "lot_size": 25},
        {"side": -1, "type": "CE", "strike": 24700, "bid": 50, "ask": 53, "mid": 51.5, "lots": 2, "lot_size": 25},
    ]
    # Expected mid: -1 * 102.5 * 50 + 1 * 51.5 * 50 = -5125 + 2575 = -2550
    # Worst: Buy at Ask (105) -> -105 * 50 = -5250; Sell at Bid (50) -> +50 * 50 = +2500 -> total = -2750
    # Slippage: | -2750 - (-2550) | = 200
    res = calculate_strategy_execution_risk(legs)
    assert res["expected_net_cashflow"] == -2550.0
    assert res["worst_net_cashflow"] == -2750.0
    assert res["slippage_exposure_inr"] == 200.0
    assert len(res["legs"]) == 2
