"""
Chronodrive Master Agent - Brand Content Orchestrator.

This is the master agent that orchestrates specialized sub-agents for
brand content creation and quality control.

Architecture:
- **Sub-Agents (3):**
  1. Brand Strategist - Expert en stratégie de marque et positionnement
  2. Social Director - Expert en création de contenu social media
  3. Brand Guardian - Garant de la cohérence de marque et contrôle qualité

- **Tools (1):**
  1. vertex_ai_rag_retrieval_tool - RAG retrieval for context-aware responses

- **Callbacks:**
  - Before-agent: Logs agent start and initializes workflow state
  - After-agent: Logs completion and finalizes state
  - Before-tool: Logs before each tool execution
  - After-tool: Logs after each tool execution

Orchestration Pattern:
- Brand Strategist: Called for brand strategy, identity, or positioning
- Social Director: Called for social media content or digital campaigns
- Brand Guardian: Called ALWAYS at the end to validate brand coherence and quality

Use this pattern for:
- Multi-agent brand content workflows
- Quality-controlled content generation
- Strategic brand communication
"""

import logging

from google.adk.agents import LlmAgent

from app.components.agents.brand_guardian.agent import (
    root_agent as brand_guardian_agent,
)
from app.components.agents.brand_strategist.agent import (
    root_agent as brand_strategist_agent,
)
from app.components.agents.social_director.agent import (
    root_agent as social_director_agent,
)
from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.components.tools.custom.vertex_ai_rag_retrieval_tool import (
    vertex_ai_rag_retrieval_tool,
)
from app.config.constants import MASTER_AGENT_DESCRIPTION, MASTER_AGENT_INSTRUCTION
from app.config.settings import settings

logger = logging.getLogger(__name__)

root_agent = LlmAgent(
    name="master_agent",
    model=settings.MODEL,
    description=MASTER_AGENT_DESCRIPTION,
    instruction=MASTER_AGENT_INSTRUCTION,
    tools=[
        vertex_ai_rag_retrieval_tool
    ],
    sub_agents=[brand_strategist_agent, social_director_agent, brand_guardian_agent],
    before_agent_callback=log_agent_start,  # Log when agent starts
    after_agent_callback=log_agent_end,  # Log when agent completes
    before_tool_callback=log_before_tool,  # Log before each tool call
    after_tool_callback=log_after_tool,  # Log after each tool call
)
