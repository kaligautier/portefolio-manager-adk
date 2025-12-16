"""BigQuery MCP Toolset Loader.

This module loads BigQuery tools from a Toolbox MCP server.
The toolbox server must be running before importing this module.

Usage:
    # Start toolbox server first:
    # cd src/app/components/agents/agent_with_big_query
    # ./start-toolbox.sh

    # Then in your agent:
    from app.components.tools.mcp.bigquery_toolset import bigquery_tools

    agent = LlmAgent(
        tools=[*bigquery_tools],
        ...
    )
"""

import logging

from toolbox_core import ToolboxSyncClient

from app.config.settings import settings


logger = logging.getLogger(__name__)


def _load_bigquery_toolset():
    """Load BigQuery toolset from Toolbox server synchronously."""
    try:
        client = ToolboxSyncClient(url=settings.TOOLBOX_BQ_URL)
        tools = client.load_toolset(settings.TOOLBOX_BQ_TOOLSET)
        logger.info(
            f"Loaded {len(tools)} tools from toolset "
            f"'{settings.TOOLBOX_BQ_TOOLSET}' at {settings.TOOLBOX_BQ_URL}"
        )
        return tools
    except Exception as e:
        logger.warning(
            f"Failed to load toolset '{settings.TOOLBOX_BQ_TOOLSET}' "
            f"from {settings.TOOLBOX_BQ_URL}: {e}"
        )
        logger.info(
            "Agent will start without BigQuery tools. "
            f"To enable, run: cd src/app/components/agents/agent_with_big_query && ./start-toolbox.sh"
        )
        return []


# Load tools at module import time using synchronous client
bigquery_tools = _load_bigquery_toolset()
