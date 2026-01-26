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

# Get project information
data "google_project" "project" {
  project_id = var.project_id
}

# Service account for the Portfolio Manager application
resource "google_service_account" "portfolio_manager" {
  account_id   = "porte-folio-manager-sa"
  display_name = "Portfolio Manager Service Account"
  description  = "Service account for Portfolio Manager Cloud Run service"
  project      = var.project_id
}

# Grant Cloud Build service account permission to deploy Cloud Run services
resource "google_project_iam_member" "cloudbuild_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"

  depends_on = [google_project_service.required_apis]
}

# Grant Cloud Build permission to act as the app service account
resource "google_service_account_iam_member" "cloudbuild_sa_user" {
  service_account_id = google_service_account.portfolio_manager.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

# Output the service account email for reference
output "service_account_email" {
  value       = google_service_account.portfolio_manager.email
  description = "Email of the Portfolio Manager service account"
}
