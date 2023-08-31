#!/bin/bash

# Setting ENV VARs
GCP_PROJECT_NAME="your-gcp-project-name"
GCP_PROJECT_REGION="your-gcp-region" # i.e. us-east1
GCP_PROJECT_ZONE="your-gcp-zone" # i.e. us-east1-b
GCP_CLUSTER_NAME="your-cluster-name"

KUBE_NAMESPACE="your-namespace-with_version" # i.e. airflow-27

# Deleting all the helm deployments for airflow 
helm delete airflow -n $KUBE_NAMESPACE

# Setting the GCP default project 
gcloud config set project $GCP_PROJECT_NAME

# Deleting the GKE Cluster
gcloud container clusters delete $GCP_CLUSTER_NAME \
--region $GCP_PROJECT_ZONE \
--async # Return immediately, without waiting for the operation in progress to complete.