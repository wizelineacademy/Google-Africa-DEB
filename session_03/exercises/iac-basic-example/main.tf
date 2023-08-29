resource "google_storage_bucket" "bucket_example" {
 name          = var.bucket_name
 location      = var.location
 storage_class = var.storage_class
 force_destroy = true

 uniform_bucket_level_access = true

 labels = {
    Name        = "My Google Cloud Storage Bucket for DSE-Africa Bootcamp 2023"
    Environment = "dev"
  }
}