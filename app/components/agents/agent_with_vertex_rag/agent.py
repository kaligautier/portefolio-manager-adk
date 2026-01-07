
import logging

from google.adk.agents import LlmAgent

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool

from app.components.tools.custom.vertex_ai_rag_retrieval_tool import (
    vertex_ai_rag_retrieval_tool,
)
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams


from app.config.constants import VERTEX_AI_RAG_DESCRIPTION, VERTEX_AI_RAG_INSTRUCTION
from app.config.settings import settings

logger = logging.getLogger(__name__)

root_agent = LlmAgent(
    name="vertex_ai_rag",
    model=settings.MODEL,
    description=VERTEX_AI_RAG_DESCRIPTION,
    instruction=VERTEX_AI_RAG_INSTRUCTION,
        tools=[
            McpToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url="http://localhost:5002/mcp"
                )
            )
        ],
    before_agent_callback=log_agent_start,  # Log when agent starts
    after_agent_callback=log_agent_end,  # Log when agent completes
    before_tool_callback=log_before_tool,  # Log before each tool call
    after_tool_callback=log_after_tool,  # Log after each tool call
)
