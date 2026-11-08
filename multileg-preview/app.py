"""
app.py - RiskOptix: Pre-Trade Multi-Leg Options Risk & Execution Engine
Flagship Quantitative Product Showcase - Modular Architecture
"""

import os
import pandas as pd
import numpy as np
import streamlit as st

# Configuration & Constants
from config import (
    DEFAULT_SPOT_PRICE,
    DEFAULT_DAYS_TO_EXPIRY,
    DEFAULT_LOT_SIZE,
    SPOT_GRID_MULTIPLIER_LOW,
    SPOT_GRID_MULTIPLIER_HIGH,
    SPOT_GRID_POINTS,
)

# Quantitative Calculation Engines
from payoff import (
    calculate_net_premium,
    calculate_strategy_payoff,
    calculate_max_profit_loss,
    find_breakevens,
)
from greeks import (
    calculate_strategy_greeks,
    calculate_today_payoff,
)
from fill_risk import (
    calculate_strategy_execution_risk,
)
from margin import (
    calculate_defined_risk_margin_estimate,
    format_broker_margin_comparison,
)

# Decoupled UI Components
from components.styles import inject_custom_css
from components.sidebar import render_sidebar
from components.hero_metrics import render_hero_metrics
from components.payoff_chart import render_payoff_chart
from components.slippage_panel import render_slippage_panel
from components.greeks_margin import render_greeks_margin_panel
from components.order_ticket import render_order_ticket
from components.failure_recovery import (
    render_anomaly_alert,
    render_failure_recovery_engine,
)


def load_option_chain() -> pd.DataFrame:
    """Loads NIFTY 50 options chain fixture or returns synthetic fallback."""
    data_path = os.path.join(os.path.dirname(__file__), "data", "nifty_options_chain.csv")
    if os.path.exists(data_path):
        return pd.read_csv(data_path)

    strikes = np.arange(24000, 25100, 100)
    return pd.DataFrame({
        "strike": strikes,
        "call_bid": [516, 424, 336, 252, 174, 107, 54, 24, 9, 3, 1],
        "call_ask": [523, 430, 341, 256, 177, 109, 56, 25, 10, 4, 2],
        "call_mid": [519, 427, 338, 254, 176, 108, 55, 25, 10, 4, 1.5],
        "call_iv": [0.15] * len(strikes),
        "call_volume": [300000] * len(strikes),
        "call_oi": [1000000] * len(strikes),
        "put_bid": [12, 19, 31, 48, 75, 114, 170, 246, 334, 428, 522],
        "put_ask": [13, 21, 33, 51, 77, 116, 173, 250, 340, 436, 532],
        "put_mid": [13, 20, 32, 49, 76, 115, 171, 248, 337, 432, 527],
        "put_iv": [0.15] * len(strikes),
        "put_volume": [300000] * len(strikes),
        "put_oi": [1000000] * len(strikes),
    })


def main():
    # Page Configuration
    st.set_page_config(
        page_title="RiskOptix | Pre-Trade Options Risk Engine",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject Fintech Theme Styles
    inject_custom_css()

    # Load Data & Constants
    df_chain = load_option_chain()
    spot_price = DEFAULT_SPOT_PRICE
    days_to_expiry = DEFAULT_DAYS_TO_EXPIRY
    lot_size = DEFAULT_LOT_SIZE
    t_years = days_to_expiry / 365.0

    # Header / Navbar
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title("⚡ RiskOptix")
        st.caption("Institutional Pre-Trade Options Risk Engine | NIFTY 50 Weekly Expiry")
    with col_h2:
        st.markdown("<div style='text-align: right; margin-top: 15px;'>", unsafe_allow_html=True)
        beginner_mode = st.toggle(
            "🎓 Beginner Mode",
            value=False,
            help="Show plain-English explanations alongside all metrics"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Sidebar Strategy Configurator
    preset, lots, user_broker_margin, legs, simulate_rejection = render_sidebar(df_chain, lot_size=lot_size)

    # Anomaly Simulation Handling
    active_legs = legs.copy()
    simulated_rejected_leg = None
    if simulate_rejection and len(legs) > 1:
        simulated_rejected_leg = active_legs.pop()

    # Quantitative Payoff Evaluations
    spot_grid = np.linspace(
        spot_price * SPOT_GRID_MULTIPLIER_LOW,
        spot_price * SPOT_GRID_MULTIPLIER_HIGH,
        SPOT_GRID_POINTS
    )
    payoffs_expiry = calculate_strategy_payoff(spot_grid, active_legs)
    max_profit, is_profit_unlimited, max_loss, is_loss_unlimited = calculate_max_profit_loss(spot_grid, payoffs_expiry)
    breakevens = find_breakevens(spot_grid, payoffs_expiry)
    net_cash_flow = calculate_net_premium(active_legs)
    payoffs_today = calculate_today_payoff(spot_grid, active_legs, time_to_expiry_years=t_years)

    # Greek Sensitivities, Fill Risk & Margin Calculations
    strategy_greeks = calculate_strategy_greeks(spot_price, active_legs, time_to_expiry_years=t_years)
    exec_risk = calculate_strategy_execution_risk(active_legs)
    margin_est = calculate_defined_risk_margin_estimate(active_legs, max_loss, is_loss_unlimited, spot_price)
    _ = format_broker_margin_comparison(user_broker_margin, max_loss, is_loss_unlimited)

    # Render Component Views
    render_anomaly_alert(simulate_rejection, simulated_rejected_leg, len(legs))

    render_hero_metrics(
        max_loss=max_loss,
        is_loss_unlimited=is_loss_unlimited,
        max_profit=max_profit,
        is_profit_unlimited=is_profit_unlimited,
        net_cash_flow=net_cash_flow,
        breakevens=breakevens,
        beginner_mode=beginner_mode
    )

    render_payoff_chart(
        spot_grid=spot_grid,
        payoffs_expiry=payoffs_expiry,
        payoffs_today=payoffs_today,
        spot_price=spot_price,
        breakevens=breakevens,
        days_to_expiry=days_to_expiry
    )

    # 2-Column Analytical Panel
    col_fill, col_meta = st.columns([1.3, 1])
    with col_fill:
        render_slippage_panel(exec_risk)
    with col_meta:
        render_greeks_margin_panel(strategy_greeks, margin_est)

    render_order_ticket(
        active_legs=active_legs,
        lots=lots,
        lot_size=lot_size,
        net_cash_flow=net_cash_flow,
        max_loss=max_loss,
        is_loss_unlimited=is_loss_unlimited,
        exec_risk=exec_risk,
        margin_est=margin_est
    )

    render_failure_recovery_engine(simulate_rejection)


if __name__ == "__main__":
    main()
