"""
models.py - Strongly Typed Domain Models for RiskOptix Options Engine
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class OptionLeg:
    """Represents an individual option leg within a multi-leg strategy."""
    side: int  # +1 for BUY (Long), -1 for SELL (Short)
    type: str  # 'CE' (Call) or 'PE' (Put)
    strike: float
    premium: float
    bid: float
    ask: float
    mid: float
    iv: float = 0.15
    volume: Optional[int] = 300000
    oi: Optional[int] = 1000000
    lots: int = 1
    lot_size: int = 25

    @property
    def side_str(self) -> str:
        return "BUY" if self.side == 1 else "SELL"

    @property
    def quantity(self) -> int:
        return self.lots * self.lot_size

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PayoffResult:
    """Encapsulates strategy terminal payoff and risk boundaries."""
    max_profit: float
    is_profit_unlimited: bool
    max_loss: float
    is_loss_unlimited: bool
    breakevens: List[float]
    net_cash_flow: float

    @property
    def direction(self) -> str:
        return "Debit" if self.net_cash_flow < 0 else "Credit"


@dataclass
class GreeksResult:
    """Portfolio net Greek sensitivities."""
    net_delta: float
    net_gamma: float
    net_theta: float
    net_vega: float


@dataclass
class LegExecutionAssessment:
    """Execution risk metrics for a single leg."""
    leg_index: int
    strike: float
    type: str
    side_str: str
    bid: float
    ask: float
    mid: float
    spread_pts: float
    spread_pct: float
    risk_level: str
    risk_color: str
    description: str
    worst_exec_price: float


@dataclass
class ExecutionRiskSummary:
    """Aggregated portfolio execution risk and slippage exposure."""
    expected_net_cashflow: float
    worst_net_cashflow: float
    slippage_exposure_inr: float
    has_high_risk_leg: bool
    legs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class MarginEstimate:
    """Defined-risk exchange SPAN margin requirement and hedge discount."""
    estimated_margin_inr: float
    hedge_benefit_inr: float
    margin_type: str
    disclaimer: str
    note: str


@dataclass
class BrokerMarginComparison:
    """Direct comparison against user broker calculator inputs."""
    broker_margin_inr: float
    capital_at_risk_ratio: str
    comparison_note: str
