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


    @app.post(
        "/run/daily",
        tags=["run", "daily"],
        summary="Run daily autonomous agentic asset manager",
    )
    async def trigger_daily(background_tasks: BackgroundTasks):
        """
        Run daily autonomous agentic asset manager using existing /run endpoint

        Returns:
            JSONResponse: Status of the daily run initiation
        """
        try:
            logger.info("Loading investment policy...")
            policy = load_default_policy()
            account_id = get_account_id_from_policy(policy)
            daily_message = get_daily_workflow_message(policy, account_id)
            logger.info("Starting autonomous daily portfolio management workflow...")
            def run_agent():
                try:
                    runner = Runner(app_name=settings.APP_NAME, agent=root_agent, session_service=app.state.session_service)

                    user_message = genai_types.Content(
                        role="user",
                        parts=[genai_types.Part(text=daily_message)]
                    )

                    logger.info("Running agent with message...")
                    event_stream = runner.run(
                        user_id="system",
                        session_id="daily_analysis",
                        new_message=user_message
                    )

                    for event in event_stream:
                        if event.content and event.content.parts:
                            logger.info(f"Event from {event.author}: {event.content.parts[0].text[:200]}...")

                    logger.info("Daily analysis completed successfully")

                except Exception as e:
                    logger.error(f"Daily analysis failed: {e}", exc_info=True)

            background_tasks.add_task(run_agent)

            return JSONResponse(
                content={
                    "status": "started",
                    "message": "Daily portfolio analysis initiated",
                    "app": settings.APP_NAME,
                    "version": settings.APP_VERSION,
                },
                status_code=202,
            )

        except Exception as e:
            logger.error(f"Failed to start daily analysis: {e}", exc_info=True)
            return JSONResponse(
                content={
                    "status": "error",
                    "message": str(e),
                },
                status_code=500,
            )


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
                "app": settings.APP_NAME,
                "version": settings.APP_VERSION,
            },
            status_code=200,
        )

    logger.info(
        f"FastAPI application created: {settings.APP_NAME} v{settings.APP_VERSION}"
    )

    return app
