output "bucket_id" {
  value       = google_storage_bucket.bucket_example.id
  description = "GCloud Bucket ID"
}

output "bucket_name" {
  value       = var.bucket_name
  description = "GCloud Bucket Name"
}

output "region" {
  value       = var.region
  description = "GCloud Region"
}

output "location" {
  value       = var.location
  description = "GCloud Zone"
}

output "project_id" {
  value       = var.project_id
  description = "GCloud Project ID"
}
