"""
Unit tests for Black-Scholes pricing, Greeks, and fill-risk engine.
"""

import pytest
import numpy as np
from greeks import (
    black_scholes_price,
    calculate_leg_greeks,
    calculate_strategy_greeks,
    calculate_today_payoff
)
from fill_risk import calculate_leg_fill_risk, calculate_strategy_execution_risk


def test_black_scholes_atm_call_put():
    """
    Test standard Black-Scholes boundary conditions:
    ATM Call Delta ~ 0.50 (with slight drift from r)
    ATM Put Delta ~ -0.50
    Call price > 0, Put price > 0
    Gamma and Vega are positive for long options.
    """
    spot = 24500.0
    strike = 24500.0
    T = 3.0 / 365.0  # 3 days
    iv = 0.135
    r = 0.065

    call_price = black_scholes_price(spot, strike, T, iv, r, "CE")
    put_price = black_scholes_price(spot, strike, T, iv, r, "PE")

    assert call_price > 50.0
    assert put_price > 50.0

    call_greeks = calculate_leg_greeks(spot, strike, T, iv, r, "CE")
    put_greeks = calculate_leg_greeks(spot, strike, T, iv, r, "PE")

    # ATM Call Delta should be around 0.50 - 0.55
    assert 0.48 <= call_greeks["delta"] <= 0.58
    # ATM Put Delta should be around -0.52 - -0.42
    assert -0.52 <= put_greeks["delta"] <= -0.42

    # Gamma and Vega must be positive
    assert call_greeks["gamma"] > 0
    assert call_greeks["vega"] > 0
    # Theta must be negative for long options (decay)
    assert call_greeks["theta"] < 0
    assert put_greeks["theta"] < 0


def test_fill_risk_liquidity_classification():
    """
    Tests spread % computation and risk classification.
    """
    # ATM liquid strike: 107 bid, 109 ask -> spread 2 pts, mid 108 -> ~1.85% (Moderate)
    res_liquid = calculate_leg_fill_risk(bid=107.5, ask=108.5, mid=108.0, volume=1200000)
    assert res_liquid["risk_level"] == "LOW"
    assert res_liquid["spread_pct"] < 1.0

    # Illiquid deep OTM wing: 0.65 bid, 1.25 ask -> spread 0.60 on 0.95 mid -> 63% (HIGH)
    res_illiquid = calculate_leg_fill_risk(bid=0.65, ask=1.25, mid=0.95, volume=20000)
    assert res_illiquid["risk_level"] == "HIGH"
    assert res_illiquid["spread_pct"] > 50.0


def test_strategy_slippage_calculation():
    """
    Tests strategy-level slippage impact (Mid vs Worst Case).
    """
    legs = [
        {"side": 1, "type": "CE", "strike": 24500.0, "bid": 107.0, "ask": 109.0, "mid": 108.0, "lots": 1, "lot_size": 25},
        {"side": -1, "type": "CE", "strike": 24700.0, "bid": 24.5, "ask": 25.75, "mid": 25.1, "lots": 1, "lot_size": 25},
    ]

    exec_risk = calculate_strategy_execution_risk(legs)
    # Expected mid cashflow: -1 * 108 * 25 + 1 * 25.1 * 25 = -2700 + 627.5 = -2072.5
    assert exec_risk["expected_net_cashflow"] == -2072.5
    # Worst case cashflow: Buy at ask (109), Sell at bid (24.5)
    # -1 * 109 * 25 + 1 * 24.5 * 25 = -2725 + 612.5 = -2112.5
    assert exec_risk["worst_net_cashflow"] == -2112.5
    # Slippage exposure in INR = abs(-2112.5 - (-2072.5)) = 40.0 INR
    assert exec_risk["slippage_exposure_inr"] == 40.0
