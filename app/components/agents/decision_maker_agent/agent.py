from google.adk.agents import LlmAgent

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.config.constants import (
    DECISION_MAKER_AGENT_DESCRIPTION,
    DECISION_MAKER_AGENT_INSTRUCTION,
)
from app.config.settings import settings


def create_agent() -> LlmAgent:
    """Factory function to create a new instance of Decision Maker Agent."""
    return LlmAgent(
        name="decision_maker_agent",
        model=settings.MODEL,
        instruction=DECISION_MAKER_AGENT_INSTRUCTION,
        description=DECISION_MAKER_AGENT_DESCRIPTION,
        tools=[],
        before_agent_callback=log_agent_start,
        after_agent_callback=log_agent_end,
        before_tool_callback=log_before_tool,
        after_tool_callback=log_after_tool,
    )
