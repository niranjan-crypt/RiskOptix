"""
styles.py - Custom Fintech UI Theming and CSS Injection for RiskOptix
"""

import streamlit as st


def inject_custom_css():
    """Injects high-contrast dark fintech stylesheet into the Streamlit session."""
    st.markdown("""
<style>
    .reportview-container {
        background-color: #0b0f19;
    }
    .metric-card {
        background: linear-gradient(135deg, #161e2e 0%, #0f172a 100%);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
    }
    .hero-loss-card {
        background: linear-gradient(135deg, #2d1217 0%, #1e1114 100%);
        border: 2px solid #ef4444;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.2);
    }
    .hero-loss-unlimited {
        background: linear-gradient(135deg, #450a0a 0%, #2a0808 100%);
        border: 3px solid #ff0055;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 85, 0.4); }
        70% { box-shadow: 0 0 0 16px rgba(255, 0, 85, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 85, 0); }
    }
    .hero-loss-title {
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #fca5a5;
        margin-bottom: 6px;
    }
    .hero-loss-value {
        font-size: 2.6rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.1;
    }
    .stat-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #94a3b8;
    }
    .stat-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #f8fafc;
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .beginner-box {
        background-color: #1e293b;
        border-left: 4px solid #38bdf8;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-top: 10px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)
