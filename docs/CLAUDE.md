# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ReAct agent built with Google's Agent Development Kit (ADK). "Bring your own agent" approach - the template handles infrastructure, deployment, and monitoring while you focus on agent business logic.

**Stack:**
- **Package Manager:** `uv` (exclusively - never use pip)
- **Agent Framework:** Google ADK
- **Backend:** FastAPI (port 8080 in production, 8000 local)
- **Model:** Gemini 2.5 Flash (Vertex AI)
- **Deployment:** Cloud Run via Cloud Build
- **Infrastructure:** Terraform (two separate configs: `iac/` and `deployment/terraform/`)
- **Observability:** Cloud Trace (always on), Cloud Logging, BigQuery, GCS

## Essential Commands

```bash
# Development
make install           # Install dependencies with uv
make playground        # Launch local playground (backend + frontend) with hot-reload
make local-backend     # Backend only on port 8000
make test              # Unit + integration tests
make lint              # codespell, ruff, mypy

# Deployment
make deploy [IAP=true] [PORT=8080]  # Direct Cloud Run deployment

# Infrastructure (iac/ directory)
cd iac
./setup-iam.sh <PROJECT_ID>         # REQUIRED FIRST TIME - Creates SA, permissions, Artifact Registry
terraform init -backend-config=init/backend.tfvars
terraform plan -var project_id=<PROJECT_ID>
terraform apply -var project_id=<PROJECT_ID>
```

## Architecture

### Agent Layer (`app/`)

**`agent.py`** - Core agent definition:
```python
from google.adk.agents import Agent
from google.adk.apps.app import App

# Tools = plain Python functions with docstrings (ADK auto-generates schemas)
def my_tool(param: str) -> str:
    """Tool description for LLM."""
    return "result"

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="Instructions here",
    tools=[my_tool],
)

app = App(root_agent=root_agent, name="app")
```

**`fast_api_app.py`** - FastAPI server:
- Uses `get_fast_api_app()` from ADK to create FastAPI with agent endpoints
- Configures telemetry, GCS bucket, Cloud SQL session storage (optional)
- Custom `/feedback` endpoint for user feedback
- CORS via `ALLOW_ORIGINS` env var

**`app_utils/`:**
- `telemetry.py`: OpenTelemetry → Cloud Trace
- `gcs.py`: Bucket creation helpers
- `typing.py`: Pydantic models

### Infrastructure (`iac/`)

**Critical Pattern:** This simplified Terraform setup uses **data sources and locals** instead of creating IAM/Artifact Registry resources, due to limited Cloud Build SA permissions.

**Setup workflow:**
1. Run `./setup-iam.sh <PROJECT_ID>` FIRST (creates SA, Artifact Registry, grants permissions)
2. Then Terraform references existing resources

**Key files:**
- `setup-iam.sh`: Creates service accounts, Artifact Registry, grants Cloud Build permissions
- `cloud_run.tf`: Cloud Run service (references SA via `local.app_service_account_email`)
- `artifact_registry.tf`: Data source for existing registry
- `iam.tf`: Local variable for SA email (no resource creation)
- `apis.tf`: Enables GCP APIs
- `cloudbuild_trigger.tf`: Creates Cloud Build trigger for auto-deployment

**Terraform State:**
- Bucket: `${PROJECT_ID}-porte-folio-manager-tfstate`
- Created by `iac/init/init.sh`

### CI/CD

**`cloudbuild.yaml`** (root) - Main pipeline:
1. Terraform init/plan/apply
2. Docker build (tagged with `$SHORT_SHA`)
3. Push to Artifact Registry
4. Deploy to Cloud Run
5. Display service URL

**Important:** Shell variables in `cloudbuild.yaml` must use `$$` (double dollar):
```yaml
- name: 'gcr.io/cloud-builders/gcloud'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      URL=$$(gcloud run services describe ...)  # Note: $$
```

**`.cloudbuild/`** - Additional pipelines:
- `staging.yaml`: Build → deploy staging → load test → trigger prod
- `deploy-to-prod.yaml`: Production deployment
- `pr_checks.yaml`: PR validation

### Deployment Infrastructure (`deployment/terraform/`)

Separate from `iac/` - full multi-environment setup with build triggers.

## Working with Agents

### Adding Tools

Tools are plain Python functions - ADK uses docstrings to generate schemas:

```python
def new_tool(location: str, date: str) -> str:
    """Get information about something.

    Args:
        location: The location to query
        date: Date in YYYY-MM-DD format

    Returns:
        Formatted string with results
    """
    return f"Results for {location} on {date}"

# Add to agent
root_agent = Agent(
    tools=[get_weather, get_current_time, new_tool],  # Add here
)
```

### Testing Locally

`make playground` launches ADK web interface with hot-reload - changes to `app/agent.py` auto-reload.

## Observability

**Two Tiers:**

1. **Agent Telemetry (Always On):** OpenTelemetry traces → Cloud Trace
2. **Prompt-Response Logging (Configurable):**
   - Local: Disabled (enable: set `LOGS_BUCKET_NAME`)
   - Deployed: Enabled with metadata only (`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT`)
   - Exported to: GCS (JSONL), BigQuery (external tables), Cloud Logging

## Critical Constraints

### Package Management
**ALWAYS use `uv`** - never pip:
```bash
uv add <package>        # Add dependency
uv add --dev <package>  # Add dev dependency
uv sync                 # Install from lock
```

### Cloud Build Variable Escaping
Shell variables need `$$`:
```yaml
# WRONG
echo "URL: $SERVICE_URL"

# CORRECT
echo "URL: $$SERVICE_URL"
```

### IAM Pattern
Due to Cloud Build SA permission limits:
- Service accounts created by `setup-iam.sh` (not Terraform)
- Terraform references via locals/data sources
- Artifact Registry created by `setup-iam.sh`
- Same applies to Cloud Build trigger (uses existing GitHub connection)

### Type Checking
Strict mypy config:
- All functions need type hints
- Disabled: `misc`, `no-untyped-call`, `no-any-return`
- First-party: `app`, `frontend`

## Environment Variables

**Required in deployed environments:**
- `GOOGLE_CLOUD_PROJECT`: Project ID
- `GOOGLE_CLOUD_LOCATION`: Default "global"
- `GOOGLE_GENAI_USE_VERTEXAI`: "True"

**Optional:**
- `LOGS_BUCKET_NAME`: Enable prompt-response logging
- `ALLOW_ORIGINS`: CORS (comma-separated)
- `DB_USER`, `DB_NAME`, `DB_PASS`, `INSTANCE_CONNECTION_NAME`: Cloud SQL
- `COMMIT_SHA`: Set by Cloud Build
- `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`: "NO_CONTENT" for privacy

## Common Workflows

### Initial Cloud Deployment
```bash
# 1. Setup IAM (one time)
cd iac
./setup-iam.sh <PROJECT_ID>

# 2. Verify resources
gcloud iam service-accounts list --filter="porte-folio-manager"
gcloud artifacts repositories list --location=europe-west1

# 3. Apply Terraform
terraform apply -var project_id=<PROJECT_ID>

# 4. Push to trigger Cloud Build
git push origin <branch>

# 5. Monitor
gcloud builds list --limit=1
```

### Adding New Agent Tool
```bash
# 1. Edit agent
vim app/agent.py

# 2. Test locally
make playground

# 3. Deploy
git commit -am "feat: add new tool"
git push  # Triggers Cloud Build auto-deployment
```

### Updating Dependencies
```bash
uv add <package>  # or edit pyproject.toml
uv sync
git add pyproject.toml uv.lock
git commit -m "deps: add <package>"
```

### Troubleshooting Cloud Build

**Check permissions:**
```bash
gcloud projects get-iam-policy <PROJECT_ID> \
  --flatten="bindings[].members" \
  --filter="bindings.members:cloudbuild"
```

**Verify resources:**
```bash
# Check Artifact Registry
gcloud artifacts repositories list --location=europe-west1

# Check Cloud Run
gcloud run services list --region=europe-west1

# View build logs
gcloud builds log <BUILD_ID>
```

**Common issues:**
1. Missing IAM permissions → Re-run `setup-iam.sh`
2. Artifact Registry doesn't exist → Created by `setup-iam.sh`, not Terraform
3. GitHub connection not found → Update `github_connection_name` variable
4. Terraform state errors → Check bucket exists: `gsutil ls gs://${PROJECT_ID}-porte-folio-manager-tfstate`

## Testing

```bash
make test  # Runs unit + integration

# Run specific test
uv run pytest tests/unit/test_agent.py
uv run pytest tests/integration/test_api.py -v

# With coverage
uv run pytest --cov=app tests/
```

Pytest config: `asyncio_default_fixture_loop_scope = "function"`

## Project Structure Note

Two separate Terraform configurations exist:
- **`iac/`**: Simplified setup for basic Cloud Run deployment (what you're using now)
- **`deployment/terraform/`**: Full multi-environment setup (staging/prod) with comprehensive configs

They serve different purposes and are not meant to be used together.
