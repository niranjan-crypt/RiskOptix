"""
greeks.py - Analytical Black-Scholes Option Pricing and Greeks Engine
Part of RiskOptix Quantitative Engine
"""

import math
from typing import Dict, List, Any, Tuple
import numpy as np

# Standard Normal CDF & PDF with pure-python fallback
try:
    from scipy.stats import norm
    def _cdf(x):
        return norm.cdf(x)
    def _pdf(x):
        return norm.pdf(x)
except ImportError:
    def _cdf(x):
        if isinstance(x, np.ndarray):
            return 0.5 * (1.0 + np.vectorize(math.erf)(x / np.sqrt(2.0)))
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    def _pdf(x):
        return np.exp(-0.5 * (x ** 2)) / np.sqrt(2.0 * math.pi)


def black_scholes_price(
    spot: float or np.ndarray,
    strike: float,
    time_to_expiry_years: float,
    volatility: float,
    risk_free_rate: float = 0.065,
    opt_type: str = "CE"
) -> float or np.ndarray:
    """
    Computes theoretical option price using Black-Scholes formula.
    """
    opt_type = opt_type.upper()
    T = max(time_to_expiry_years, 1e-6)
    vol = max(volatility, 1e-4)

    d1 = (np.log(spot / strike) + (risk_free_rate + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)

    discount = np.exp(-risk_free_rate * T)

    if opt_type in ("CE", "CALL"):
        price = spot * _cdf(d1) - strike * discount * _cdf(d2)
    elif opt_type in ("PE", "PUT"):
        price = strike * discount * _cdf(-d2) - spot * _cdf(-d1)
    else:
        raise ValueError(f"Unknown option type: {opt_type}")

    return np.maximum(price, 0.0)


def calculate_leg_greeks(
    spot: float,
    strike: float,
    time_to_expiry_years: float,
    volatility: float,
    risk_free_rate: float = 0.065,
    opt_type: str = "CE"
) -> Dict[str, float]:
    """
    Calculates single-unit Black-Scholes Greeks:
    Delta, Gamma, Theta (per day decay in ₹), and Vega (per 1% IV shift in ₹).
    """
    opt_type = opt_type.upper()
    T = max(time_to_expiry_years, 1e-6)
    vol = max(volatility, 1e-4)

    d1 = (math.log(spot / strike) + (risk_free_rate + 0.5 * vol ** 2) * T) / (vol * math.sqrt(T))
    d2 = d1 - vol * math.sqrt(T)

    pdf_d1 = _pdf(d1)
    discount = math.exp(-risk_free_rate * T)

    # Gamma & Vega are identical for Calls and Puts
    gamma = pdf_d1 / (spot * vol * math.sqrt(T))
    vega = (spot * pdf_d1 * math.sqrt(T)) / 100.0  # per 1% move in IV

    if opt_type in ("CE", "CALL"):
        delta = _cdf(d1)
        theta_annual = -(spot * pdf_d1 * vol) / (2 * math.sqrt(T)) - (risk_free_rate * strike * discount * _cdf(d2))
    else:
        delta = _cdf(d1) - 1.0
        theta_annual = -(spot * pdf_d1 * vol) / (2 * math.sqrt(T)) + (risk_free_rate * strike * discount * _cdf(-d2))

    theta_daily = theta_annual / 365.0

    return {
        "delta": round(float(delta), 4),
        "gamma": round(float(gamma), 6),
        "theta": round(float(theta_daily), 2),
        "vega": round(float(vega), 2),
    }


def calculate_strategy_greeks(
    spot: float,
    legs: List[Dict[str, Any]],
    time_to_expiry_years: float,
    risk_free_rate: float = 0.065
) -> Dict[str, float]:
    """
    Aggregates net portfolio Greeks across all strategy legs.
    Weights each Greek by side (+1 / -1), number of lots, and lot size.
    """
    net_delta = 0.0
    net_gamma = 0.0
    net_theta = 0.0
    net_vega = 0.0

    for leg in legs:
        side = leg["side"]
        lots = leg.get("lots", 1)
        lot_size = leg.get("lot_size", 25)
        multiplier = side * lots * lot_size
        iv = leg.get("iv", 0.14)

        greeks = calculate_leg_greeks(
            spot=spot,
            strike=leg["strike"],
            time_to_expiry_years=time_to_expiry_years,
            volatility=iv,
            risk_free_rate=risk_free_rate,
            opt_type=leg["type"]
        )

        net_delta += multiplier * greeks["delta"]
        net_gamma += multiplier * greeks["gamma"]
        net_theta += multiplier * greeks["theta"]
        net_vega += multiplier * greeks["vega"]

    return {
        "net_delta": round(net_delta, 2),
        "net_gamma": round(net_gamma, 4),
        "net_theta": round(net_theta, 2),
        "net_vega": round(net_vega, 2)
    }


def calculate_today_payoff(
    spot_grid: np.ndarray,
    legs: List[Dict[str, Any]],
    time_to_expiry_years: float,
    risk_free_rate: float = 0.065
) -> np.ndarray:
    """
    Computes theoretical P&L today across spot grid (T-0 curve).
    Payoff today = sum( side * lots * lot_size * (Theoretical_Price(S_grid) - entry_premium) )
    """
    today_payoff = np.zeros_like(spot_grid, dtype=float)

    for leg in legs:
        side = leg["side"]
        lots = leg.get("lots", 1)
        lot_size = leg.get("lot_size", 25)
        entry_p = leg["premium"]
        iv = leg.get("iv", 0.14)

        theo_prices = black_scholes_price(
            spot=spot_grid,
            strike=leg["strike"],
            time_to_expiry_years=time_to_expiry_years,
            volatility=iv,
            risk_free_rate=risk_free_rate,
            opt_type=leg["type"]
        )

        leg_today_pnl = side * lots * lot_size * (theo_prices - entry_p)
        today_payoff += leg_today_pnl

    return today_payoff
