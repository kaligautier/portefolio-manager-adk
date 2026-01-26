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

# Artifact Registry repository for Docker images
resource "google_artifact_registry_repository" "portfolio_manager" {
  location      = var.region
  repository_id = "porte-folio-manager-repo"
  description   = "Docker repository for Portfolio Manager application"
  format        = "DOCKER"
  project       = var.project_id

  depends_on = [google_project_service.required_apis]
}

# Output the repository details
output "artifact_registry_repository" {
  value       = google_artifact_registry_repository.portfolio_manager.name
  description = "Full name of the Artifact Registry repository"
}
