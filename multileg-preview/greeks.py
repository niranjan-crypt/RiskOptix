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
