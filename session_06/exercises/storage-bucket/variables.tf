terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.5.0"
    }
  }
  required_version = ">= 1.4.6"
}

variable "project_id" {
  type          = string
  description   = "The Project ID in which will be deployed the services"
}

variable "location" {
  type          = string
  description   = "General location for deployments"
}

variable "region" {
  type          = string
  description   = "The region in which the GCP bucket will be created."
}

variable "zone" {
  type          = string
  description   = "The zone in which the GCP bucket will be created."
}

variable "bucket_name" {
  type          = string
  description   = "The name of the GCP bucket to create."
}

variable "storage_class" {
  type          = string
  default       = "STANDARD"
  description   = "The type of storage "
}

variable "environment" {
  type          = string
  default       = "dev"
  description   = "Environment definition"
}