
import logging

import google.auth
from google.adk.agents import LlmAgent
from google.adk.auth.auth_credential import AuthCredentialTypes
from google.adk.tools.bigquery.bigquery_credentials import BigQueryCredentialsConfig
from google.adk.tools.bigquery.bigquery_toolset import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.config.constants import AGENT_BQ_DESCRIPTION, AGENT_BQ_INSTRUCTION
from app.config.settings import settings

logger = logging.getLogger(__name__)

# Define the desired credential type
# By default use Application Default Credentials (ADC)
CREDENTIALS_TYPE = None

# Define BigQuery tool config with write mode set to allowed
# Note: In production, consider using BLOCKED (read-only) or PROTECTED mode
tool_config = BigQueryToolConfig(
    write_mode=WriteMode.ALLOWED,
    application_name=settings.PROJECT_NAME  # Use PROJECT_NAME (no spaces)
)

# Initialize credentials based on type
if CREDENTIALS_TYPE == AuthCredentialTypes.OAUTH2:
    # Use settings for OAuth credentials if configured
    credentials_config = BigQueryCredentialsConfig(
        client_id=settings.BIGQUERY_CLIENT_ID if hasattr(settings, 'BIGQUERY_CLIENT_ID') else None,
        client_secret=settings.BIGQUERY_CLIENT_SECRET if hasattr(settings, 'BIGQUERY_CLIENT_SECRET') else None,
    )
elif CREDENTIALS_TYPE == AuthCredentialTypes.SERVICE_ACCOUNT:
    # Use service account credentials if specified
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
    name="agent_native_bq",
    model=settings.MODEL,
    description=AGENT_BQ_DESCRIPTION,
    instruction=AGENT_BQ_INSTRUCTION,
    tools=[bigquery_toolset],  # Pass the instantiated toolset, not the class
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
