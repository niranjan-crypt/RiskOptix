"""
test_models.py - Unit Tests for Strongly Typed Domain Models
"""

import pytest
from models import OptionLeg, PayoffResult, GreeksResult


def test_option_leg_properties():
    """Validates OptionLeg property derivations and serialization."""
    leg = OptionLeg(
        side=1,
        type="CE",
        strike=24500.0,
        premium=100.0,
        bid=99.0,
        ask=101.0,
        mid=100.0,
        lots=2,
        lot_size=25
    )

    assert leg.side_str == "BUY"
    assert leg.quantity == 50
    d = leg.to_dict()
    assert d["strike"] == 24500.0
    assert d["lots"] == 2


def test_payoff_result_direction():
    """Validates direction debit vs credit determination."""
    p_debit = PayoffResult(
        max_profit=5000.0,
        is_profit_unlimited=False,
        max_loss=-2000.0,
        is_loss_unlimited=False,
        breakevens=[24600.0],
        net_cash_flow=-2500.0
    )
    assert p_debit.direction == "Debit"

    p_credit = PayoffResult(
        max_profit=2500.0,
        is_profit_unlimited=False,
        max_loss=-5000.0,
        is_loss_unlimited=False,
        breakevens=[24300.0, 24700.0],
        net_cash_flow=1500.0
    )
    assert p_credit.direction == "Credit"
