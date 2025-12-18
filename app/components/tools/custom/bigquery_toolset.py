import google.auth
from google.adk.tools.bigquery.bigquery_toolset import (
    BigQueryCredentialsConfig,
    BigQueryToolConfig,
    BigQueryToolset,
)

from app.config.settings import settings

# Define BigQuery tool config
tool_config = BigQueryToolConfig(
    application_name=settings.PROJECT_NAME,
    compute_project_id="lil-onboard-gcp",
)

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
