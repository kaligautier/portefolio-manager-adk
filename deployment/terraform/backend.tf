terraform {
  backend "gcs" {
    bucket = "lil-onboard-gcp-terraform-state"
    prefix = "portefolio-manager-adk/prod"
  }
}
