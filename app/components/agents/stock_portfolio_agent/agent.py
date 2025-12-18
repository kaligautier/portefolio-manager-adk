from google.adk.agents import LlmAgent

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.components.tools.custom.bigquery_toolset import bigquery_toolset
from app.config.constants import (
    STOCK_PORTFOLIO_AGENT_DESCRIPTION,
    STOCK_PORTFOLIO_AGENT_INSTRUCTION,
)
from app.config.settings import settings

root_agent = LlmAgent(
    name="stock_portfolio_agent",
    model=settings.MODEL,
    instruction=STOCK_PORTFOLIO_AGENT_INSTRUCTION,
    description=STOCK_PORTFOLIO_AGENT_DESCRIPTION,
    tools=[bigquery_toolset],
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
