"""
Agents package - Exposes all available agents.

This module centralizes access to all agents in the application:
- Master Agent: Orchestrates brand content creation with sub-agents
- Brand Strategist: Expert in brand strategy and positioning
- Social Director: Expert in social media content creation
- Brand Guardian: Brand coherence and quality control
- Google Search Agent: Performs web searches
- Agent with BigQuery Toolbox: BigQuery operations using MCP tools
- Agent with Native BigQuery: BigQuery operations using native tools
- Agent with PostgreSQL: PostgreSQL database operations
- Agent with Tools: Generic agent with custom tools
- Agent with Vertex AI Search: Vertex AI search capabilities
- Agent with Vertex RAG: Vertex AI RAG retrieval
- Parallel Agent: Executes tasks in parallel
- Sequential and Loop Agent: Executes tasks sequentially with loops
"""

from app.components.agents.agent_with_native_bq.agent import (
    root_agent as agent_with_native_bq,
)
from app.components.agents.agent_with_tools.agent import root_agent as agent_with_tools
from app.components.agents.agent_with_vertex_ai_search.agent import (
    root_agent as agent_with_vertex_ai_search,
)
from app.components.agents.agent_with_vertex_rag.agent import (
    root_agent as agent_with_vertex_rag,
)
from app.components.agents.google_search_agent.agent import (
    root_agent as google_search_agent,
)
from app.components.agents.parralel_agent.agent import root_agent as parallel_agent
from app.components.agents.seq_and_loop_agent.agent import (
    root_agent as seq_and_loop_agent,
)

__all__ = [
    "agent_with_native_bq",
    "agent_with_tools",
    "agent_with_vertex_ai_search",
    "agent_with_vertex_rag",
    "brand_guardian_agent",
    "brand_strategist_agent",
    "google_search_agent",
    "parallel_agent",
    "seq_and_loop_agent",
]
