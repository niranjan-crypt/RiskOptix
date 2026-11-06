"""
config.py - Centralized Configuration and Constants for RiskOptix
"""

# Underlying Instrument Parameters
DEFAULT_SPOT_PRICE: float = 24500.0
DEFAULT_DAYS_TO_EXPIRY: int = 3
DEFAULT_LOT_SIZE: int = 25  # Official NSE NIFTY 50 Lot Size
RISK_FREE_RATE: float = 0.07  # 7% annual risk-free rate for Black-Scholes

# Grid Configuration for Numerical Payoff Evaluation
SPOT_GRID_MULTIPLIER_LOW: float = 0.85
SPOT_GRID_MULTIPLIER_HIGH: float = 1.15
SPOT_GRID_POINTS: int = 601

# UI Color Palette & Theme Tokens
COLOR_PRIMARY = "#38bdf8"       # Sky blue
COLOR_SUCCESS = "#10b981"       # Emerald green
COLOR_WARNING = "#f59e0b"       # Amber
COLOR_DANGER = "#ef4444"        # Crimson / red
COLOR_BG_DARK = "#0b0f19"       # Deep slate background
COLOR_CARD_BG = "#0f172a"       # Card surface background
COLOR_BORDER = "#1e293b"        # Subdued border line
COLOR_ACCENT_PINK = "#ec4899"   # Breakeven annotation pink

# Preset Strategy Names
PRESET_IRON_CONDOR = "Iron Condor (4-Leg, Defined Risk)"
PRESET_BULL_CALL_SPREAD = "Bull Call Spread (2-Leg, Defined Debit)"
PRESET_BEAR_PUT_SPREAD = "Bear Put Spread (2-Leg, Defined Debit)"
PRESET_SHORT_STRADDLE = "Short Straddle (2-Leg, UNLIMITED Risk)"
PRESET_LONG_STRANGLE = "Long Strangle (2-Leg, Volatility Play)"
PRESET_CUSTOM = "Custom Multi-Leg (Build from scratch)"

STRATEGY_PRESETS = [
    PRESET_IRON_CONDOR,
    PRESET_BULL_CALL_SPREAD,
    PRESET_BEAR_PUT_SPREAD,
    PRESET_SHORT_STRADDLE,
    PRESET_LONG_STRANGLE,
    PRESET_CUSTOM,
]
