"""
components package - Modular UI components for RiskOptix Streamlit Dashboard
"""

from .styles import inject_custom_css
from .sidebar import render_sidebar
from .hero_metrics import render_hero_metrics
from .payoff_chart import render_payoff_chart
from .slippage_panel import render_slippage_panel
from .greeks_margin import render_greeks_margin_panel
from .order_ticket import render_order_ticket
from .failure_recovery import render_failure_recovery_engine

__all__ = [
    "inject_custom_css",
    "render_sidebar",
    "render_hero_metrics",
    "render_payoff_chart",
    "render_slippage_panel",
    "render_greeks_margin_panel",
    "render_order_ticket",
    "render_failure_recovery_engine",
]
