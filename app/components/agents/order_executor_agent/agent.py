from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.config.constants import (
    ORDER_EXECUTOR_AGENT_DESCRIPTION,
    ORDER_EXECUTOR_AGENT_INSTRUCTION,
)
from app.config.settings import settings


def create_agent() -> LlmAgent:
    """Factory function to create a new instance of Order Executor Agent."""
    return LlmAgent(
        name="order_executor_agent",
        model=settings.MODEL,
        instruction=ORDER_EXECUTOR_AGENT_INSTRUCTION,
        description=ORDER_EXECUTOR_AGENT_DESCRIPTION,
        tools=[
            McpToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url="http://localhost:5002/mcp"
                )
            )
        ],
        before_agent_callback=log_agent_start,
        after_agent_callback=log_agent_end,
        before_tool_callback=log_before_tool,
        after_tool_callback=log_after_tool,
    )
