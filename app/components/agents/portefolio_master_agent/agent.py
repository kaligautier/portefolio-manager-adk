import logging

from google.adk.agents import LlmAgent

from app.components.agents.market_specialist_agent import (
    root_agent as market_specialist_agent,
)
from app.components.agents.stock_portfolio_agent import (
    root_agent as stock_portfolio_agent,
)
from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.config.constants import (
    PORTEFOLIO_MANAGER_AGENT_DESCRIPTION,
    PORTEFOLIO_MANAGER_AGENT_INSTRUCTION,
)
from app.config.settings import settings

logger = logging.getLogger(__name__)

root_agent = LlmAgent(
    name="portefolio_master_agent",
    model=settings.MODEL,
    description=PORTEFOLIO_MANAGER_AGENT_DESCRIPTION,
    instruction=PORTEFOLIO_MANAGER_AGENT_INSTRUCTION,
    tools=[],
    sub_agents=[
        stock_portfolio_agent,
        market_specialist_agent,
    ],
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
