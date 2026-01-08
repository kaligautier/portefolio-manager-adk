"""FastAPI application factory."""

import logging

from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import JSONResponse
from google.adk import Runner
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from app.components.agents.portefolio_master_agent.agent import root_agent
from app.config.constants import get_daily_workflow_message
from app.config.settings import settings
from app.utils.policy_loader import load_default_policy, get_account_id_from_policy

logger = logging.getLogger(__name__)

logger.info(f"✓ Root agent loaded: {root_agent.name}")
logger.info(f"✓ Sequential workflow with {len(root_agent.sub_agents)} sub-agents")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""

    session_service_uri = None
    if settings.USE_AGENT_ENGINE_SESSIONS and settings.AGENT_ENGINE_ID:
        session_service_uri = f"agentengine://{settings.AGENT_ENGINE_ID}"
        logger.info(f"Using Vertex AI Agent Engine Sessions: {settings.AGENT_ENGINE_ID}")
    else:
        logger.info("Using InMemorySessionService (sessions not persisted)")

    app: FastAPI = get_fast_api_app(
        agents_dir=settings.AGENT_DIR,
        web=True,
        session_service_uri=session_service_uri,
    )

    app.title = settings.APP_NAME
    app.description = settings.APP_DESCRIPTION
    app.version = settings.APP_VERSION
    app.state.session_service = InMemorySessionService()

    @app.get("/health", tags=["Health"], summary="Health Check")
    async def health_check():
        """
        Health check endpoint for monitoring systems.

        Returns:
            JSONResponse: A simple JSON response with status "ok"
        """
        return JSONResponse(
            content={
                "status": "ok",
                "app": app.title,
                "version": app.version,
            },
            status_code=200,
        )

    logger.info(
        f"FastAPI application created: {app.title} v{app.version}"
    )

    return app
