
import logging

from google.adk.agents import LlmAgent

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool

from app.components.tools.custom.vertex_search_tool import (
    vertex_search_tool,
)

from app.config.constants import VERTEX_AI_SEARCH_DESCRIPTION, VERTEX_AI_SEARCH_INSTRUCTION
from app.config.settings import settings

logger = logging.getLogger(__name__)

root_agent = LlmAgent(
    name="vertex_ai_search_agent",
    model=settings.MODEL,
    description=VERTEX_AI_SEARCH_DESCRIPTION,
    instruction=VERTEX_AI_SEARCH_INSTRUCTION,
    tools=[
        vertex_search_tool,  
    ],
    before_agent_callback=log_agent_start,  # Log when agent starts
    after_agent_callback=log_agent_end,  # Log when agent completes
    before_tool_callback=log_before_tool,  # Log before each tool call
    after_tool_callback=log_after_tool,  # Log after each tool call
)
