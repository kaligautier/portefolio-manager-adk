"""
TO DO .. 
"""

import logging

from google.adk.agents import LlmAgent

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.config.constants import (
    AGENT_BRAND_STRATEGIST_DESCRIPTION,
    AGENT_BRAND_STRATEGIST_INSTRUCTION,
)
from app.config.settings import settings

logger = logging.getLogger(__name__)

root_agent = LlmAgent(
    name="brand_strategist",
    model=settings.MODEL,
    description=AGENT_BRAND_STRATEGIST_DESCRIPTION,
    instruction=AGENT_BRAND_STRATEGIST_INSTRUCTION,
    tools=[],
    sub_agents=[],
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
