import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from google.genai import types

from app.utils.error import ConfigurationError


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    Configuration is loaded from:
    1. Environment variables
    2. .env file (in non-Docker environments)
    3. Default values defined below
    All settings are type-safe and validated by Pydantic.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    if not os.getenv("DOCKER_ENV"):
        load_dotenv(find_dotenv(".env"))

    APP_NAME: str = Field(
        default="ADK_Agent_Template",
        description="Application name displayed in API documentation",
    )

    APP_DESCRIPTION: str = Field(
        default="Production-ready ADK agent template with best practices",
        description="Application description for API documentation",
    )

    APP_VERSION: str = Field(
        default="0.1.0",
        description="Application version",
    )

    PROJECT_NAME: str = Field(
        default="adk-agent-template",
        description="Project identifier used in paths and naming",
    )

    HOST: str = Field(
        default="0.0.0.0",
        description="Server host address (0.0.0.0 for all interfaces)",
    )
    PORT: int = Field(
        default=8000,
        description="Server port",
    )
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode (disable in production)",
    )

    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    AGENT_NAME: str = Field(
        default="template_agent",
        description="Primary agent name",
    )

    @property
    def RETRY_CONFIG(self) -> types.HttpRetryOptions:
        """Get the HTTP retry configuration."""
        return types.HttpRetryOptions(
            attempts=5,
            exp_base=7,
            initial_delay=1,
            http_status_codes=[429, 500, 503, 504],
        )

    MODEL: str = Field(
        default="gemini-2.5-flash",
        description="AI model to use for the agent",
    )

    @property
    def AGENT_DIR(self) -> str:
        """Get the absolute path to the agents directory."""
        return str(Path(__file__).parent.parent / "components" / "agents")

    @property
    def INSTRUCTIONS_DIR(self) -> str:
        """Get the absolute path to the instructions templates directory."""
        return str(Path(__file__).parent.parent / "instructions" / "templates")

    GOOGLE_GENAI_USE_VERTEXAI: bool = Field(
        default=True,
        description="Enable Vertex AI for Google Generative AI (required)",
    )

    GOOGLE_API_KEY: str = Field(
        default="",
        description="Google Generative AI API key for non-Vertex AI authentication",
    )

    GOOGLE_CLOUD_PROJECT: str = Field(
        default="lil-onboard-gcp",
        description="GCP project ID (required)",
    )

    GOOGLE_CLOUD_LOCATION: str = Field(
        default="europe-west1",
        description="GCP region (e.g., us-central1, europe-west1)",
    )

    USER_ID: str = Field(
        default="api_user",
        description="Default user ID for session management",
    )

    RAG_CORPUS_ID: str = Field(
        default="projects/lil-onboard-gcp/locations/europe-west1/ragCorpora/2227030015734710272",
        description=(
            "Vertex AI RAG Corpus resource name "
            "(format: projects/PROJECT_ID/locations/LOCATION/"
            "ragCorpora/CORPUS_ID)"
        ),
    )

    SEARCH_DATASTORE_ID: str = Field(
        default="projects/lil-onboard-gcp/locations/eu/collections/default_collection/dataStores/chrono-factory_1765276748374_google_drive",
        description=(
            "Vertex AI Search datastore ID "
            "(format: projects/PROJECT_ID/locations/LOCATION/"
            "collections/default_collection/dataStores/DATASTORE_ID)"
        ),
    )

    TOOLBOX_PG_URL: str = Field(
        default="http://127.0.0.1:5000",
        description="Toolbox MCP server URL for loading external tools",
    )

    TOOLBOX_PG_TOOLSET: str = Field(
        default="postgres_database_tools",
        description="Name of the PostgreSQL toolset to load from Toolbox server",
    )

    BIGQUERY_PROJECT: str = Field(
        default="lil-onboard-gcp",
        description="GCP project ID for BigQuery",
    )

    BIGQUERY_LOCATION: str = Field(
        default="",
        description="BigQuery location (optional, e.g., US, EU)",
    )

    BIGQUERY_USE_CLIENT_OAUTH: bool = Field(
        default=False,
        description="Use client OAuth for BigQuery authentication",
    )

    TOOLBOX_BQ_URL: str = Field(
        default="http://127.0.0.1:5001",
        description="Toolbox MCP server URL for BigQuery tools",
    )

    TOOLBOX_BQ_TOOLSET: str = Field(
        default="bigquery_database_tools",
        description="Name of the BigQuery toolset to load from Toolbox server",
    )

    TOOLBOX_IBKR_URL: str = Field(
        default="http://127.0.0.1:5002",  # Assuming a different port for IBKR MCP
        description="Toolbox MCP server URL for IBKR tools",
    )

    TOOLBOX_IBKR_TOOLSET: str = Field(
        default="ibkr_tools",
        description="Name of the IBKR toolset to load from Toolbox server",
    )

    AGENT_ENGINE_ID: str = Field(
        default="",
        description=(
            "Vertex AI Agent Engine (Reasoning Engine) ID for managed sessions. "
            "Format: projects/PROJECT_ID/locations/LOCATION/reasoningEngines/ENGINE_ID"
        ),
    )
    USE_AGENT_ENGINE_SESSIONS: bool = Field(
        default=False,
        description="Enable Vertex AI Agent Engine Sessions (fully managed on GCP)",
    )

try:
    settings = Settings()
except ValidationError as e:
    raise ConfigurationError(
        message="Configuration validation failed",
        details={"pydantic_errors": e.errors()},
    ) from e