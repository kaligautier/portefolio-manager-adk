import google.auth
from google.adk.agents import LlmAgent
from google.adk.auth.auth_credential import AuthCredentialTypes
from google.adk.tools.bigquery.bigquery_credentials import BigQueryCredentialsConfig
from google.adk.tools.bigquery.bigquery_toolset import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.config.constants import (
    REAL_ESTATE_AGENT_DESCRIPTION,
    REAL_ESTATE_AGENT_INSTRUCTION,
)
from app.config.settings import settings

CREDENTIALS_TYPE = None
tool_config = BigQueryToolConfig(
    write_mode=WriteMode.ALLOWED,
    application_name=settings.PROJECT_NAME  # Use PROJECT_NAME (no spaces)
)

if CREDENTIALS_TYPE == AuthCredentialTypes.OAUTH2:
    # Use settings for OAuth credentials if configured
    credentials_config = BigQueryCredentialsConfig(
        client_id=settings.BIGQUERY_CLIENT_ID if hasattr(settings, 'BIGQUERY_CLIENT_ID') else None,
        client_secret=settings.BIGQUERY_CLIENT_SECRET if hasattr(settings, 'BIGQUERY_CLIENT_SECRET') else None,
    )
elif CREDENTIALS_TYPE == AuthCredentialTypes.SERVICE_ACCOUNT:
    creds, _ = google.auth.load_credentials_from_file("service_account_key.json")
    credentials_config = BigQueryCredentialsConfig(credentials=creds)
else:
    # Use Application Default Credentials (ADC)
    application_default_credentials, _ = google.auth.default()
    credentials_config = BigQueryCredentialsConfig(
        credentials=application_default_credentials
    )

# Instantiate the BigQuery toolset with credentials and config
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config,
    bigquery_tool_config=tool_config
)

root_agent = LlmAgent(
    name="real_estate_specialist_agent",
    model=settings.MODEL,
    instruction=REAL_ESTATE_AGENT_INSTRUCTION,
    description=REAL_ESTATE_AGENT_DESCRIPTION,
    tools=[bigquery_toolset],
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
