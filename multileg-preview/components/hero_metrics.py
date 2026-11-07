"""
hero_metrics.py - High-Prominence Risk KPI Banner for RiskOptix
"""

import streamlit as st
from typing import List


def render_hero_metrics(
    max_loss: float,
    is_loss_unlimited: bool,
    max_profit: float,
    is_profit_unlimited: bool,
    net_cash_flow: float,
    breakevens: List[float],
    beginner_mode: bool = False
):
    """
    Renders top row hero metric cards with Max Loss prioritized in largest typography.
    """
    c_hero, c_stat1, c_stat2, c_stat3 = st.columns([1.5, 1, 1, 1])

    with c_hero:
        if is_loss_unlimited:
            st.markdown("""
            <div class="hero-loss-unlimited">
                <div class="hero-loss-title">⚠️ MAXIMUM LOSS</div>
                <div class="hero-loss-value" style="color: #ff3366;">UNLIMITED</div>
                <div style="color: #fca5a5; font-size: 0.8rem; margin-top: 5px;">Unbounded risk! Strategy can trigger total margin liquidation.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="hero-loss-card">
                <div class="hero-loss-title">MAXIMUM LOSS</div>
                <div class="hero-loss-value">₹{abs(max_loss):,.0f}</div>
                <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 5px;">Strictly capped by outer hedge wings.</div>
            </div>
            """, unsafe_allow_html=True)

    with c_stat1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="stat-title">Maximum Profit</div>', unsafe_allow_html=True)
        if is_profit_unlimited:
            st.markdown('<div class="stat-value" style="color: #10b981;">UNLIMITED</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="stat-value" style="color: #10b981;">+₹{max_profit:,.0f}</div>', unsafe_allow_html=True)
        st.caption("Best-case payoff at expiration")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_stat2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="stat-title">Net Cash Flow</div>', unsafe_allow_html=True)
        if net_cash_flow < 0:
            st.markdown(f'<div class="stat-value" style="color: #38bdf8;">-₹{abs(net_cash_flow):,.0f}</div>', unsafe_allow_html=True)
            st.caption("Net Debit (Paid upfront)")
        else:
            st.markdown(f'<div class="stat-value" style="color: #34d399;">+₹{net_cash_flow:,.0f}</div>', unsafe_allow_html=True)
            st.caption("Net Credit (Collected upfront)")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_stat3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="stat-title">Breakeven Points</div>', unsafe_allow_html=True)
        if len(breakevens) == 2:
            st.markdown(f'<div class="stat-value" style="font-size: 1.3rem;">{breakevens[0]} & {breakevens[1]}</div>', unsafe_allow_html=True)
            st.caption("2 Zero-crossing boundaries")
        elif len(breakevens) == 1:
            st.markdown(f'<div class="stat-value">{breakevens[0]}</div>', unsafe_allow_html=True)
            st.caption("1 Zero-crossing boundary")
        else:
            st.markdown('<div class="stat-value">None</div>', unsafe_allow_html=True)
            st.caption("No breakeven inside range")
        st.markdown('</div>', unsafe_allow_html=True)

    if beginner_mode:
        st.markdown("""
        <div class="beginner-box">
            💡 <b>Beginner Guide:</b><br>
            • <b>Max Loss:</b> The absolute worst-case loss you can incur, regardless of where the market closes on expiry day.<br>
            • <b>Net Debit vs Credit:</b> A Debit means cash leaves your account now to buy options; a Credit means you collect cash upfront by selling.<br>
            • <b>Breakeven:</b> The exact index price where your trade makes exactly ₹0 profit and ₹0 loss.
        </div>
        """, unsafe_allow_html=True)
