from google.adk.agents import LlmAgent

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.config.constants import (
    PORTFOLIO_EVALUATOR_AGENT_DESCRIPTION,
    PORTFOLIO_EVALUATOR_AGENT_INSTRUCTION,
)
from app.config.settings import settings


def create_agent() -> LlmAgent:
    """Factory function to create a new instance of Portfolio Evaluator Agent."""
    return LlmAgent(
        name="portfolio_evaluator_agent",
        model=settings.MODEL,
        instruction=PORTFOLIO_EVALUATOR_AGENT_INSTRUCTION,
        description=PORTFOLIO_EVALUATOR_AGENT_DESCRIPTION,
        tools=[],
        output_key="risk_assessment", 
        before_agent_callback=log_agent_start,
        after_agent_callback=log_agent_end,
        before_tool_callback=log_before_tool,
        after_tool_callback=log_after_tool,
    )
