# Apache Airflow Helm Deployment

This repository contains resources and scripts to deploy a basic Apache Airflow using Helm charts on Google Cloud Platform (GCP).

## Requirements

- [GCP account](https://console.cloud.google.com/) 
- [Kubectl](https://kubernetes.io/docs/reference/kubectl/kubectl/)
- [Helm](https://helm.sh/docs/intro/install/)
- [gcloud SDK](https://cloud.google.com/sdk/docs/install-sdk)
- The gcloud project must have the following APIs enabled:
        - Compute Engine
        - Kubernetes Engine

## Getting Started

Follow these steps to deploy Apache Airflow on GCP:

1. Clone this repository.
2. Go to the folder:

```shell
cd session_02/exercises/airflow-helm-deployment
```

2.1. OPTIONAL: To modify values in `values.yaml` got to

```shell
cd charts/airflow
```

3. Change the permissions for both `./scripts/deploy.sh` and `./scripts/teradown.sh`

```sh
chmod +x scripts/deploy.sh scripts/teardown.sh
```

4. Run the deployment script before you modify your ENV VARs. To decide what's the best region/zone to use visit [GCP Region Picker](https://cloud.withgoogle.com/region-picker/)

```sh
./scripts/deploy.sh
```

6. Access to the [Airflow WEB UI](https://localhost:8080/)

6. After the deployment and the exercises, destroy all the resources created:

```sh
./scripts/teardown.sh
```