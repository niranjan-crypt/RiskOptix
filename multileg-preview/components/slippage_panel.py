"""
slippage_panel.py - Execution Fill-Risk & Bid-Ask Slippage Analysis Panel
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any


def render_slippage_panel(exec_risk: Dict[str, Any]):
    """
    Renders the fill-risk breakdown table and execution slippage alerts.
    """
    st.subheader("🎯 Fill-Risk & Bid-Ask Slippage Panel")
    st.caption("Calculates worst-case execution price (Buy at Ask, Sell at Bid) to quantify market impact.")

    leg_data = []
    for l in exec_risk["legs"]:
        leg_data.append({
            "Leg": f"L{l['leg_index']}",
            "Position": f"{l['side_str']} {l['strike']} {l['type']}",
            "Bid / Ask": f"₹{l['bid']} / ₹{l['ask']}",
            "Spread %": f"{l['spread_pct']}%",
            "Fill Risk": l["risk_level"],
            "Worst Execution": f"₹{l['worst_exec_price']}"
        })

    df_legs = pd.DataFrame(leg_data)
    st.dataframe(df_legs, hide_index=True, use_container_width=True)

    worst_vs_expected = exec_risk["slippage_exposure_inr"]
    if exec_risk["has_high_risk_leg"]:
        st.warning(
            f"⚠️ **High Spread Warning:** One or more legs have wide bid-ask spreads! "
            f"In the worst case, your strategy will suffer an extra **₹{worst_vs_expected:,.0f}** in execution slippage."
        )
    else:
        st.info(
            f"✅ **Liquidity Healthy:** All selected legs have tight bid-ask spreads. "
            f"Estimated maximum market order slippage is capped at **₹{worst_vs_expected:,.0f}**."
        )
