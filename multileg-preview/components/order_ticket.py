"""
order_ticket.py - Pre-Trade Commitment Confirmation Summary and Actions
"""

import streamlit as st
from typing import List, Dict, Any


def render_order_ticket(
    active_legs: List[Dict[str, Any]],
    lots: int,
    lot_size: int,
    net_cash_flow: float,
    max_loss: float,
    is_loss_unlimited: bool,
    exec_risk: Dict[str, Any],
    margin_est: Dict[str, Any]
):
    """
    Renders Screen 4 Pre-Confirmation summary ticket and submission buttons.
    """
    st.markdown("---")
    st.subheader("📋 Pre-Trade Commitment Summary")

    direction = "Debit" if net_cash_flow < 0 else "Credit"
    loss_str = "UNLIMITED" if is_loss_unlimited else f"₹{abs(max_loss):,.0f}"
    worst_vs_expected = exec_risk.get("slippage_exposure_inr", 0.0)

    st.info(f"""
**Trader Commitment Statement:**  
You are preparing to submit **{len(active_legs)} legs** on **NIFTY 50** ({lots} lots / {lots * lot_size} qty).  
• **Net {direction}:** ₹{abs(net_cash_flow):,.0f}  
• **Maximum Capital at Risk:** {loss_str}  
• **Worst-Case Fill Price:** ₹{abs(exec_risk['worst_net_cashflow']):,.0f} (maximum ₹{worst_vs_expected:,.0f} slippage)  
• **Approx. Margin Block:** ₹{margin_est['estimated_margin_inr']:,.0f}
""")

    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
    with btn_col1:
        confirm_click = st.button("🚀 Confirm & Send Basket", type="primary", use_container_width=True)
    with btn_col2:
        cancel_click = st.button("❌ Cancel Order", use_container_width=True)

    if confirm_click:
        st.success("✅ Basket order submitted to execution router. (Telemetry event logged: `order_confirmed`)")
    if cancel_click:
        st.warning("Order cancelled. No capital deployed.")
