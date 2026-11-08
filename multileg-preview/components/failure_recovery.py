"""
failure_recovery.py - Execution Anomaly Simulation & Decision Engine
"""

import streamlit as st
from typing import Dict, Any, Optional, List


def render_anomaly_alert(
    simulate_leg_rejection: bool,
    simulated_rejected_leg: Optional[Dict[str, Any]],
    total_legs: int
):
    """Renders prominent banner if a partial fill / leg rejection anomaly is simulated."""
    if simulate_leg_rejection and simulated_rejected_leg:
        side_str = "BUY" if simulated_rejected_leg.get("side") == 1 else "SELL"
        strike = simulated_rejected_leg.get("strike")
        opt_type = simulated_rejected_leg.get("type")
        st.error(
            f"🚨 **EXECUTION ALERT**: Leg {total_legs} ({side_str} {strike} {opt_type}) "
            f"was **REJECTED** by Exchange (Freeze Limit / Liquidity Exceeded)! "
            f"Showing naked post-failure risk profile."
        )


def render_failure_recovery_engine(simulate_leg_rejection: bool):
    """
    Renders Screen 5: 3-tier execution recovery options for unhedged legs.
    """
    if not simulate_leg_rejection:
        return

    st.markdown("---")
    st.subheader("🛡️ Leg Failure Decision Engine (Trade-off Analysis)")
    st.markdown("""
    When an exchange rejects or partially fills a multi-leg strategy, traders are instantly exposed to unhedged directional risk.
    Below are the 3 execution recovery options defined in the RiskOptix Execution Architecture:
    """)

    opt_c1, opt_c2, opt_c3 = st.columns(3)
    with opt_c1:
        st.markdown("""
        **Option 1: Cancel All Remaining Legs**
        - **Pros:** Predictable, stops further execution mistakes.
        - **Cons:** Leaves already-filled legs naked in the market.
        """)
        if st.button("Execute: Cancel Remaining"):
            st.warning("All pending legs cancelled. Filled legs flagged for manual square-off.")

    with opt_c2:
        st.markdown("""
        **Option 2: Immediate Market Retry**
        - **Pros:** Preserves intended multi-leg hedge structure.
        - **Cons:** Market prices may have moved; high slippage.
        """)
        if st.button("Execute: Retry Leg at Market"):
            st.info("Retrying failed strike at market limit band...")

    with opt_c3:
        st.markdown("""
        **Option 3: Hedge-First Ordering (Recommended)**
        - **Pros:** Buys protective wing first; zero naked exposure.
        - **Cons:** Slightly slower basket fill latency (~120ms).
        """)
        if st.button("Execute: Re-order Hedge-First"):
            st.success("Hedge-first protection enabled. Margin safeguarded.")
