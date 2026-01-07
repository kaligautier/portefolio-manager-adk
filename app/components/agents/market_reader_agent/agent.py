from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.components.tools.custom.ibkr_account_tool import get_my_account_id
from app.config.constants import (
    MARKET_READER_AGENT_DESCRIPTION,
    MARKET_READER_AGENT_INSTRUCTION,
)
from app.config.settings import settings


def create_agent() -> LlmAgent:
    """Factory function to create a new instance of Market Reader Agent."""
    return LlmAgent(
        name="market_reader_agent",
        model=settings.MODEL,
        instruction=MARKET_READER_AGENT_INSTRUCTION,
        description=MARKET_READER_AGENT_DESCRIPTION,
        tools=[
            get_my_account_id,
            McpToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url=settings.IBKR_MCP_URL
                )
            ),
        ],
        before_agent_callback=log_agent_start,
        after_agent_callback=log_agent_end,
        before_tool_callback=log_before_tool,
        after_tool_callback=log_after_tool,
    )
