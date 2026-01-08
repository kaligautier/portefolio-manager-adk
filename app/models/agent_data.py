"""Pydantic models for structured data exchange between agents."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

class Position(BaseModel):
    """Individual position in the portfolio."""

    symbol: str = Field(..., description="Stock ticker symbol (e.g., AAPL)")
    conid: Optional[int] = Field(None, description="IBKR contract ID")
    quantity: float = Field(..., description="Number of shares held")
    market_value: float = Field(..., description="Current market value in USD")
    average_cost: Optional[float] = Field(
        None, description="Average cost per share in USD"
    )
    unrealized_pnl: Optional[float] = Field(
        None, description="Unrealized profit/loss in USD"
    )
    unrealized_pnl_percent: Optional[float] = Field(
        None, description="Unrealized PnL as percentage"
    )
    sector: Optional[str] = Field(None, description="Sector classification")


class PortfolioSnapshot(BaseModel):
    """Portfolio snapshot from IBKR Reader Agent."""

    account_id: str = Field(..., description="IBKR account ID")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Snapshot timestamp"
    )
    positions: List[Position] = Field(default_factory=list, description="All positions")
    total_market_value: float = Field(..., description="Total portfolio value in USD")
    cash: float = Field(..., description="Available cash in USD")
    buying_power: Optional[float] = Field(None, description="Available buying power")
    realized_pnl: Optional[float] = Field(None, description="Realized PnL")
    unrealized_pnl: Optional[float] = Field(None, description="Total unrealized PnL")


class MarketCondition(str, Enum):
    """Overall market trend."""

    BULL = "BULL"
    BEAR = "BEAR"
    NEUTRAL = "NEUTRAL"


class PositionMarketData(BaseModel):
    """Market data for a single position."""

    symbol: str = Field(..., description="Stock ticker symbol")
    current_price: float = Field(..., description="Current market price")
    volatility_30d: Optional[float] = Field(
        None, description="30-day annualized volatility (%)"
    )
    trend_30d: Optional[float] = Field(None, description="30-day price change (%)")
    trend_60d: Optional[float] = Field(None, description="60-day price change (%)")
    trend_90d: Optional[float] = Field(None, description="90-day price change (%)")
    sector: Optional[str] = Field(None, description="Sector classification")
    sector_performance: Optional[str] = Field(
        None, description="Sector performance analysis"
    )


class MarketAnalysis(BaseModel):
    """Market analysis from Market Reader Agent."""

    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Analysis timestamp"
    )
    vix_level: Optional[float] = Field(None, description="VIX volatility index level")
    vix_interpretation: Optional[str] = Field(
        None, description="VIX interpretation (Low/Normal/High/Extreme)"
    )
    market_trend: MarketCondition = Field(..., description="Overall market trend")
    positions_data: List[PositionMarketData] = Field(
        default_factory=list, description="Market data for each position"
    )
    market_summary: str = Field(..., description="Brief market conditions summary")


class RiskLevel(str, Enum):
    """Risk level classification."""

    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PositionRisk(BaseModel):
    """Risk assessment for a single position."""

    symbol: str = Field(..., description="Stock ticker symbol")
    concentration_percent: float = Field(
        ..., description="Position concentration as % of portfolio"
    )
    is_over_concentrated: bool = Field(
        ..., description="True if exceeds concentration limits"
    )
    at_stop_loss: bool = Field(..., description="True if hit stop loss threshold")
    at_take_profit: bool = Field(..., description="True if hit take profit threshold")
    risk_level: RiskLevel = Field(..., description="Overall risk level for position")
    recommendation: Optional[str] = Field(
        None, description="Risk mitigation recommendation"
    )


class RiskAssessment(BaseModel):
    """Risk assessment from Portfolio Evaluator Agent."""

    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Assessment timestamp"
    )
    current_drawdown: float = Field(..., description="Current drawdown (%)")
    max_drawdown_limit: float = Field(..., description="Maximum allowed drawdown (%)")
    is_over_drawdown_limit: bool = Field(
        ..., description="True if exceeds max drawdown"
    )
    total_exposure: float = Field(..., description="Total portfolio exposure")
    positions_risk: List[PositionRisk] = Field(
        default_factory=list, description="Risk for each position"
    )
    overall_risk_level: RiskLevel = Field(..., description="Overall portfolio risk")
    allocation_drift: Optional[dict] = Field(
        None, description="Drift from target allocation"
    )
    risk_summary: str = Field(..., description="Brief risk assessment summary")


class DecisionAction(str, Enum):
    """Decision actions."""

    HOLD = "HOLD"
    REINFORCE = "REINFORCE"
    ROTATE = "ROTATE"
    CUT_LOSERS = "CUT_LOSERS"
    REBALANCE = "REBALANCE"


class TradeAction(str, Enum):
    """Trade action type."""

    BUY = "BUY"
    SELL = "SELL"


class Trade(BaseModel):
    """Individual trade to execute."""

    symbol: str = Field(..., description="Stock ticker symbol")
    action: TradeAction = Field(..., description="BUY or SELL")
    quantity: int = Field(..., description="Number of shares")
    limit_price: Optional[float] = Field(
        None, description="Limit price (None for market price)"
    )
    rationale: str = Field(..., description="Reason for this trade")


class DecisionPlan(BaseModel):
    """Decision plan from Decision Maker Agent."""

    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Decision timestamp"
    )
    decision_action: DecisionAction = Field(..., description="Overall decision action")
    rationale: str = Field(..., description="Rationale for the decision")
    trades: List[Trade] = Field(
        default_factory=list, description="List of trades to execute"
    )
    expected_outcome: Optional[str] = Field(
        None, description="Expected portfolio outcome"
    )
    risk_considerations: Optional[str] = Field(
        None, description="Risk considerations for this decision"
    )


class OrderStatusEnum(str, Enum):
    """Order execution status."""

    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class OrderStatus(BaseModel):
    """Status of an executed order."""

    symbol: str = Field(..., description="Stock ticker symbol")
    action: TradeAction = Field(..., description="BUY or SELL")
    quantity: int = Field(..., description="Number of shares")
    limit_price: Optional[float] = Field(None, description="Limit price used")
    conid: Optional[int] = Field(None, description="IBKR contract ID")
    order_id: Optional[str] = Field(None, description="IBKR order ID")
    status: OrderStatusEnum = Field(..., description="Execution status")
    message: str = Field(..., description="Confirmation or error message")


class ExecutionSummary(BaseModel):
    """Execution summary from Order Executor Agent."""

    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Execution timestamp"
    )
    account_id: str = Field(..., description="IBKR account ID")
    execution_status: str = Field(
        ..., description="Overall status (COMPLETED/PARTIAL/NONE/FAILED)"
    )
    orders: List[OrderStatus] = Field(
        default_factory=list, description="Status of all orders"
    )
    total_submitted: int = Field(0, description="Total orders submitted")
    total_successful: int = Field(0, description="Successfully executed orders")
    total_failed: int = Field(0, description="Failed orders")
    errors: List[str] = Field(default_factory=list, description="Errors encountered")
    estimated_portfolio_value: Optional[float] = Field(
        None, description="Estimated portfolio value after execution"
    )
    execution_summary: str = Field(..., description="Brief execution summary")
