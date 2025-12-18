from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.config.constants import (
    MARKET_SPECIALIST_AGENT_DESCRIPTION,
    MARKET_SPECIALIST_AGENT_INSTRUCTION,
)
from app.config.settings import settings

root_agent = LlmAgent(
    name="market_specialist_agent",
    model=settings.MODEL,
    instruction=MARKET_SPECIALIST_AGENT_INSTRUCTION,
    description=MARKET_SPECIALIST_AGENT_DESCRIPTION,
    tools=[google_search],
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
