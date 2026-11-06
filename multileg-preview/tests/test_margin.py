"""
test_margin.py - Unit Tests for SPAN and Defined-Risk Margin Estimator
"""

import pytest
from margin import (
    calculate_defined_risk_margin_estimate,
    format_broker_margin_comparison,
)


def test_defined_risk_margin():
    """Hedged spread should calculate defined loss plus buffer with hedge discount."""
    legs = [{"side": 1, "lots": 2, "lot_size": 25}]
    max_loss = -5000.0
    res = calculate_defined_risk_margin_estimate(legs, max_loss, is_loss_unlimited=False, spot_price=24500.0)

    assert res["estimated_margin_inr"] == 5750.0  # 5000 + 15% buffer
    assert res["margin_type"] == "DEFINED RISK (Hedged Spread)"
    assert res["hedge_benefit_inr"] > 0


def test_unlimited_risk_margin():
    """Unbounded position should trigger full contract SPAN margin."""
    legs = [{"side": -1, "lots": 2, "lot_size": 25}]
    res = calculate_defined_risk_margin_estimate(legs, max_loss=float("-inf"), is_loss_unlimited=True, spot_price=24500.0)

    # 24500 * 50 = 1,225,000 contract value
    # ~13.5% = 165,375
    assert res["estimated_margin_inr"] > 100000.0
    assert "UNBOUNDED RISK" in res["margin_type"]
    assert res["hedge_benefit_inr"] == 0.0


def test_broker_margin_comparison():
    """Validates capital at risk percentage against user broker input."""
    res = format_broker_margin_comparison(broker_margin_input=50000.0, max_loss=-25000.0, is_loss_unlimited=False)
    assert res["capital_at_risk_ratio"] == "50.0%"
    assert "fully covered" in res["comparison_note"]
