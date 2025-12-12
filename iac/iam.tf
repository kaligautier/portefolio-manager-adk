# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Service account email for the Portfolio Manager application
# Note: This service account must be created manually first with:
# cd iac && ./setup-iam.sh YOUR_PROJECT_ID

locals {
  app_service_account_email = "porte-folio-manager-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Output the service account email for reference
output "service_account_email" {
  value       = local.app_service_account_email
  description = "Email of the Portfolio Manager service account"
}
