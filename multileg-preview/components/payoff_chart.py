"""
payoff_chart.py - Interactive Multi-Curve Payoff Visualization using Plotly
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from typing import List


def render_payoff_chart(
    spot_grid: np.ndarray,
    payoffs_expiry: np.ndarray,
    payoffs_today: np.ndarray,
    spot_price: float,
    breakevens: List[float],
    days_to_expiry: int = 3
):
    """
    Renders interactive Plotly payoff curve with profit/loss fill zones,
    T-0 time-decay curve, spot marker, and breakeven boundaries.
    """
    st.subheader("📈 Interactive Strategy Payoff Curve")

    fig = go.Figure()

    # Profit zone shading
    fig.add_trace(go.Scatter(
        x=spot_grid,
        y=np.maximum(payoffs_expiry, 0),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.12)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Profit Zone',
        hoverinfo='skip'
    ))

    # Loss zone shading
    fig.add_trace(go.Scatter(
        x=spot_grid,
        y=np.minimum(payoffs_expiry, 0),
        fill='tozeroy',
        fillcolor='rgba(239, 68, 68, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Loss Zone',
        hoverinfo='skip'
    ))

    # Expiry Payoff line
    fig.add_trace(go.Scatter(
        x=spot_grid,
        y=payoffs_expiry,
        mode='lines',
        name='Payoff at Expiry',
        line=dict(color='#38bdf8', width=3.5)
    ))

    # Today (T-0) Payoff line
    fig.add_trace(go.Scatter(
        x=spot_grid,
        y=payoffs_today,
        mode='lines',
        name=f'Payoff Today (T-{days_to_expiry}d)',
        line=dict(color='#f59e0b', width=2, dash='dot')
    ))

    # Zero line
    fig.add_hline(y=0, line_dash="solid", line_color="#475569", line_width=1)

    # Current Spot line
    fig.add_vline(
        x=spot_price,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text=f"Current Spot ({spot_price})",
        annotation_position="top left"
    )

    # Breakeven Markers
    for be in breakevens:
        fig.add_vline(
            x=be,
            line_dash="dot",
            line_color="#ec4899",
            annotation_text=f"BE: {be}",
            annotation_position="bottom right"
        )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0b0f19',
        height=420,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(title="NIFTY 50 Spot Price at Expiry", gridcolor="#1e293b"),
        yaxis=dict(title="Net P&L (₹)", gridcolor="#1e293b", zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)
