
import logging

from google.adk.agents import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.tools.function_tool import FunctionTool
from google.adk.agents.sequential_agent import SequentialAgent

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool

from app.config.settings import settings
from google.adk.tools import google_search

logger = logging.getLogger(__name__)

root_agent = LlmAgent(
    name="google_search_agent",
    model=settings.MODEL,
    description="""AGENT_GOOGLE_SEARCH_DESCRIPTION""",
    instruction="""Tu sais faire des recherches Google pour aider à répondre aux questions de l'utilisateur.""",
    tools=[google_search],
    sub_agents=[],
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
