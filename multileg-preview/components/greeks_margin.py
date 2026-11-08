"""
greeks_margin.py - Net Greeks and SPAN Margin Requirements Panel
"""

import streamlit as st
from typing import Dict, Any


def render_greeks_margin_panel(
    strategy_greeks: Dict[str, Any],
    margin_est: Dict[str, Any]
):
    """
    Renders portfolio net Greeks sensitivities and exchange margin estimation.
    """
    st.subheader("⚖️ Net Greeks & Margin Estimate")

    # Greeks Row
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    g_col1.metric("Delta (Δ)", f"{strategy_greeks['net_delta']}")
    g_col2.metric("Gamma (Γ)", f"{strategy_greeks['net_gamma']}")
    g_col3.metric("Theta (Θ)", f"₹{strategy_greeks['net_theta']}/d")
    g_col4.metric("Vega (ν)", f"₹{strategy_greeks['net_vega']}/1%")

    st.markdown("---")
    st.markdown("**Margin Requirements & Hedge Benefit:**")

    m_c1, m_c2 = st.columns(2)
    with m_c1:
        st.metric("Estimated Margin", f"₹{margin_est['estimated_margin_inr']:,.0f}")
        st.caption(f"Category: {margin_est['margin_type']}")
    with m_c2:
        st.metric("Hedge Discount", f"₹{margin_est['hedge_benefit_inr']:,.0f}")
        st.caption("Capital saved by hedged wings")

    st.caption(f"ℹ️ *{margin_est['disclaimer']}*")
