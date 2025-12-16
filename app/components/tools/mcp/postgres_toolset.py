"""PostgreSQL MCP Toolset Loader.

This module loads PostgreSQL tools from a Toolbox MCP server.
The toolbox server must be running before importing this module.

Usage:
    # Start toolbox server first:
    # toolbox serve --config postgres.yaml --port 5000

    # Then in your agent:
    from app.components.tools.mcp.postgres_toolset import postgres_tools

    agent = LlmAgent(
        tools=[*postgres_tools],
        ...
    )
"""

import logging

from toolbox_core import ToolboxSyncClient

from app.config.settings import settings


logger = logging.getLogger(__name__)


def _load_postgres_toolset():
    """Load PostgreSQL toolset from Toolbox server synchronously."""
    try:
        client = ToolboxSyncClient(url=settings.TOOLBOX_PG_URL)
        tools = client.load_toolset(settings.TOOLBOX_PG_TOOLSET)
        logger.info(
            f"Loaded {len(tools)} tools from toolset "
            f"'{settings.TOOLBOX_PG_TOOLSET}' at {settings.TOOLBOX_PG_URL}"
        )
        return tools
    except Exception as e:
        logger.warning(
            f"Failed to load toolset '{settings.TOOLBOX_PG_TOOLSET}' "
            f"from {settings.TOOLBOX_PG_URL}: {e}"
        )
        logger.info(
            "Agent will start without PostgreSQL tools. "
            f"To enable, run: toolbox serve --tools-file postgres.yaml --port {settings.TOOLBOX_PG_URL.split(':')[-1]}"
        )
        return []


postgres_tools = _load_postgres_toolset()
