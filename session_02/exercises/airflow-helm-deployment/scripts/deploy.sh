#!/bin/bash

# Setting ENV VARs
GCP_PROJECT_NAME="your-gcp-project-name"
GCP_PROJECT_REGION="your-gcp-region" # i.e. us-east1
GCP_PROJECT_ZONE="your-gcp-zone" # i.e. us-east1-b
GCP_CLUSTER_NAME="your-cluster-name"

KUBE_NAMESPACE="your-namespace-with_version" # i.e. airflow-27

# Setting the GCP default project 
gcloud config set project $GCP_PROJECT_NAME

# Creating the Cluster
gcloud container clusters create $GCP_CLUSTER_NAME \
--machine-type n1-standard-4 \
--num-nodes 1 \
--region $GCP_PROJECT_ZONE

# To autenticate kubectl we're going to use gcloud to get the credentials to our cluster
gcloud container clusters get-credentials $GCP_CLUSTER_NAME --region $GCP_PROJECT_ZONE

# Let's create the namespace and add the latest apache-airflow repo available
kubectl create namespace $KUBE_NAMESPACE
helm repo add apache-airflow https://airflow.apache.org

# Deploy our airflow chart within our GKE cluster
helm upgrade --install airflow apache-airflow/airflow -n $KUBE_NAMESPACE --debug

# Changing the post-forward to access it from outside 
kubectl port-forward svc/airflow-webserver 8080:8080 -n $KUBE_NAMESPACE