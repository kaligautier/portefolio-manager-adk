#!/bin/sh
# This script performs a health check for the API Gateway service.
# It checks if the API Gateway is reachable and returns any valid response.

# Use localhost for healthcheck from inside the container
URL="https://localhost:5055/v1/api/iserver/auth/status"

echo "Attempting to check API Gateway health at: $URL"

# Use curl to get the HTTP status code and save the response body to a temporary file.
# -s: Silent mode (don't show progress meter or error messages)
# -k: Allow insecure server connections when using SSL (useful for local development with self-signed certs)
# -w "%{http_code}": Output only the HTTP status code
# -o /tmp/api_response.json: Write the response body to this file
STATUS=$(curl -sk -w "%{http_code}" -o /tmp/api_response.json "$URL")

# Check if the HTTP status code indicates the Gateway is responding
# We accept any response between 200-499 (including 401/403 unauthorized)
# This means the Gateway is UP even if not authenticated
if [ "$STATUS" -ge 200 ] && [ "$STATUS" -lt 500 ]; then
  echo "API Gateway healthcheck successful: HTTP status $STATUS, Gateway is responding."
  exit 0 # Exit with 0 for success
else
  echo "API Gateway healthcheck failed: Received HTTP status $STATUS."
  exit 1 # Exit with 1 for failure
fi
