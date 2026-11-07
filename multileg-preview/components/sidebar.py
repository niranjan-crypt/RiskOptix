"""
sidebar.py - Strategy Configurator and Parameter Controls
"""

import streamlit as st
import pandas as pd
from typing import Tuple, List, Dict, Any


def get_option_row(df_chain: pd.DataFrame, strike: float) -> pd.Series:
    """Helper to locate row in options chain or fallback to ATM."""
    match = df_chain[df_chain["strike"] == strike]
    if not match.empty:
        return match.iloc[0]
    return df_chain.iloc[len(df_chain) // 2]


def render_sidebar(
    df_chain: pd.DataFrame,
    lot_size: int = 25
) -> Tuple[str, int, float, List[Dict[str, Any]], bool]:
    """
    Renders strategy preset selector, lot inputs, and custom builder.
    Returns:
        (preset, lots, user_broker_margin, legs, simulate_leg_rejection)
    """
    st.sidebar.header("🛠️ Strategy Configurator")

    presets = [
        "Iron Condor (4-Leg, Defined Risk)",
        "Bull Call Spread (2-Leg, Defined Debit)",
        "Bear Put Spread (2-Leg, Defined Debit)",
        "Short Straddle (2-Leg, UNLIMITED Risk)",
        "Long Strangle (2-Leg, Volatility Play)",
        "Custom Multi-Leg (Build from scratch)"
    ]

    preset = st.sidebar.selectbox("Choose Strategy Preset", presets)
    lots = st.sidebar.number_input("Number of Lots", min_value=1, max_value=100, value=2, step=1)
    user_broker_margin = st.sidebar.number_input(
        "Broker SPAN Margin (Option A, ₹)",
        min_value=0.0,
        value=75000.0,
        step=5000.0,
        help="Enter the margin shown in your broker calculator for comparison"
    )

    legs: List[Dict[str, Any]] = []

    if preset == "Iron Condor (4-Leg, Defined Risk)":
        r1 = get_option_row(df_chain, 24100)
        r2 = get_option_row(df_chain, 24300)
        r3 = get_option_row(df_chain, 24700)
        r4 = get_option_row(df_chain, 24900)
        legs = [
            {"side": 1, "type": "PE", "strike": 24100, "bid": r1["put_bid"], "ask": r1["put_ask"], "mid": r1["put_mid"], "premium": r1["put_mid"], "iv": r1["put_iv"], "volume": r1["put_volume"], "lots": lots, "lot_size": lot_size},
            {"side": -1, "type": "PE", "strike": 24300, "bid": r2["put_bid"], "ask": r2["put_ask"], "mid": r2["put_mid"], "premium": r2["put_mid"], "iv": r2["put_iv"], "volume": r2["put_volume"], "lots": lots, "lot_size": lot_size},
            {"side": -1, "type": "CE", "strike": 24700, "bid": r3["call_bid"], "ask": r3["call_ask"], "mid": r3["call_mid"], "premium": r3["call_mid"], "iv": r3["call_iv"], "volume": r3["call_volume"], "lots": lots, "lot_size": lot_size},
            {"side": 1, "type": "CE", "strike": 24900, "bid": r4["call_bid"], "ask": r4["call_ask"], "mid": r4["call_mid"], "premium": r4["call_mid"], "iv": r4["call_iv"], "volume": r4["call_volume"], "lots": lots, "lot_size": lot_size},
        ]

    elif preset == "Bull Call Spread (2-Leg, Defined Debit)":
        r1 = get_option_row(df_chain, 24500)
        r2 = get_option_row(df_chain, 24700)
        legs = [
            {"side": 1, "type": "CE", "strike": 24500, "bid": r1["call_bid"], "ask": r1["call_ask"], "mid": r1["call_mid"], "premium": r1["call_mid"], "iv": r1["call_iv"], "volume": r1["call_volume"], "lots": lots, "lot_size": lot_size},
            {"side": -1, "type": "CE", "strike": 24700, "bid": r2["call_bid"], "ask": r2["call_ask"], "mid": r2["call_mid"], "premium": r2["call_mid"], "iv": r2["call_iv"], "volume": r2["call_volume"], "lots": lots, "lot_size": lot_size},
        ]

    elif preset == "Bear Put Spread (2-Leg, Defined Debit)":
        r1 = get_option_row(df_chain, 24500)
        r2 = get_option_row(df_chain, 24300)
        legs = [
            {"side": 1, "type": "PE", "strike": 24500, "bid": r1["put_bid"], "ask": r1["put_ask"], "mid": r1["put_mid"], "premium": r1["put_mid"], "iv": r1["put_iv"], "volume": r1["put_volume"], "lots": lots, "lot_size": lot_size},
            {"side": -1, "type": "PE", "strike": 24300, "bid": r2["put_bid"], "ask": r2["put_ask"], "mid": r2["put_mid"], "premium": r2["put_mid"], "iv": r2["put_iv"], "volume": r2["put_volume"], "lots": lots, "lot_size": lot_size},
        ]

    elif preset == "Short Straddle (2-Leg, UNLIMITED Risk)":
        r1 = get_option_row(df_chain, 24500)
        legs = [
            {"side": -1, "type": "CE", "strike": 24500, "bid": r1["call_bid"], "ask": r1["call_ask"], "mid": r1["call_mid"], "premium": r1["call_mid"], "iv": r1["call_iv"], "volume": r1["call_volume"], "lots": lots, "lot_size": lot_size},
            {"side": -1, "type": "PE", "strike": 24500, "bid": r1["put_bid"], "ask": r1["put_ask"], "mid": r1["put_mid"], "premium": r1["put_mid"], "iv": r1["put_iv"], "volume": r1["put_volume"], "lots": lots, "lot_size": lot_size},
        ]

    elif preset == "Long Strangle (2-Leg, Volatility Play)":
        r1 = get_option_row(df_chain, 24700)
        r2 = get_option_row(df_chain, 24300)
        legs = [
            {"side": 1, "type": "CE", "strike": 24700, "bid": r1["call_bid"], "ask": r1["call_ask"], "mid": r1["call_mid"], "premium": r1["call_mid"], "iv": r1["call_iv"], "volume": r1["call_volume"], "lots": lots, "lot_size": lot_size},
            {"side": 1, "type": "PE", "strike": 24300, "bid": r2["put_bid"], "ask": r2["put_ask"], "mid": r2["put_mid"], "premium": r2["put_mid"], "iv": r2["put_iv"], "volume": r2["put_volume"], "lots": lots, "lot_size": lot_size},
        ]

    else:
        st.sidebar.subheader("Configure Legs")
        num_legs = st.sidebar.slider("Number of Legs", 1, 4, 2)
        available_strikes = df_chain["strike"].tolist()
        for i in range(num_legs):
            st.sidebar.markdown(f"**Leg {i+1}**")
            col_s1, col_s2, col_s3 = st.sidebar.columns(3)
            with col_s1:
                side_str = st.selectbox(f"Side L{i+1}", ["BUY", "SELL"], key=f"side_{i}")
            with col_s2:
                type_str = st.selectbox(f"Type L{i+1}", ["CE", "PE"], key=f"type_{i}")
            with col_s3:
                strike_val = st.selectbox(
                    f"Strike L{i+1}",
                    available_strikes,
                    index=min(5 + i * 2, len(available_strikes) - 1),
                    key=f"strike_{i}"
                )

            r = get_option_row(df_chain, strike_val)
            prefix = "call" if type_str == "CE" else "put"
            side_val = 1 if side_str == "BUY" else -1

            legs.append({
                "side": side_val,
                "type": type_str,
                "strike": strike_val,
                "bid": r[f"{prefix}_bid"],
                "ask": r[f"{prefix}_ask"],
                "mid": r[f"{prefix}_mid"],
                "premium": r[f"{prefix}_mid"],
                "iv": r[f"{prefix}_iv"],
                "volume": r[f"{prefix}_volume"],
                "lots": lots,
                "lot_size": lot_size
            })

    # Leg-Failure Simulation Toggle
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚠️ Execution Anomaly Simulation")
    simulate_leg_rejection = st.sidebar.checkbox(
        "Simulate Partial Fill / Leg 4 Rejection",
        value=False,
        help="Demonstrates what happens to your risk profile if the exchange rejects a hedging leg."
    )

    return preset, lots, user_broker_margin, legs, simulate_leg_rejection
