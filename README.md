
# Table of Contents

1.  [Contains of this repo](#org0d0e966)
2.  [Terraform K8s Cluster in GKE](#org09042a6)
        1.  [Prerequisites](#org45279bd)
        2.  [Dependencies](#org8ee0988)
        3.  [Installing](#org9258179)
    1.  [Terraform destruction](#org6c9260b)
3.  [Airflow](#org3602e04)
    1.  [Prerequisites](#org20c49db)
    2.  [Dependencies](#org2b7a974)
    3.  [NFS preparation](#org25c21bd)
    4.  [Storage](#org626c3e1)
    5.  [Airflow Installation](#org274dad7)
    6.  [Accessing to Airflow dashboard](#org959018f)
4.  [Acknowledgments](#org5427e61)

This repository contains some of the principal resourses that you probably want to use when starts working into the IaC module.


<a id="org0d0e966"></a>

# Contains of this repo

    .
    └── terraforms-templates
        ├── gcp
        │   ├── modules
        │   │   ├── cloudsql
        │   │   ├── compute-engine
        │   │   ├── gke
        │   │   └── vpc
        │   └── nfs
        └── kubernetes


<a id="org09042a6"></a>

# Terraform K8s Cluster in GKE

The current architecture was implemented following this guide [Provision a GKE Cluster guide](https://learn.hashicorp.com/tutorials/terraform/gke?in=terraform/kubernetes) )


<a id="org45279bd"></a>

### Prerequisites

-   GCP account configured
-   Kubectl cli


<a id="org8ee0988"></a>

### Dependencies

-   gcloud cli
-   Cluster Version: 1.20
-   Terraform >= 0.13


<a id="org9258179"></a>

### Installing

Go to the directory `gcp/` and execute the following Terraform commands:

    terraform init
    terraform apply --var-file=terraform.tfvars

Once that the cluster is created (it will took a few minutes), set the kubectl context:

    gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw location)


<a id="org6c9260b"></a>

## Terraform destruction

To destroy the EKS cluster with all the services, we run:

    terraform destroy --var-file=terraform.tfvars

**Important notes**
Remember that you are working with services on the cloud and you are creating the infraestructure to work with between them. Often times, due different conditions, including internet desconections and server problems, some of your services will stay in your Cloud Provider, so, we encourage you to check twice everytime you run this feature and make sure that all the services were shut down properly.


<a id="org3602e04"></a>

# Airflow


<a id="org20c49db"></a>

## Prerequisites

-   Helm 3


<a id="org2b7a974"></a>

## Dependencies

-   kubernetes cluster version: 1.20


<a id="org25c21bd"></a>

## NFS preparation

To work with Airflow we will use a NFS servicem we will create it in the Kubernetes cluster.

First create a namespace for the nsf server executing in your respective cloud provider path:

    kubectl create namespace nfs

then is time to create the nfs server using your *yaml file*:

    kubectl -n nfs apply -f nfs/nfs-server.yaml

now export the nfs server:

    export NFS_SERVER=$(kubectl -n nfs get service/nfs-server -o jsonpath="{.spec.clusterIP}")

finally, in order to install Airflow, go to the directory `kubernetes/`:


<a id="org626c3e1"></a>

## Storage

Create a namespace for storage deployment:

    kubectl create namespace storage

Add the chart for the nfs-provisioner

    helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/

Install nfs-external-provisioner

    helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
        --namespace storage \
        --set nfs.server=$NFS_SERVER \
        --set nfs.path=/


<a id="org274dad7"></a>

## Airflow Installation

Here we are using official Airflow helm chart as example, but, can also been installed any other Airflow distribution.

Create the namespace

    kubectl create namespace airflow

Add the chart repository and confirm:

    helm repo add apache-airflow https://airflow.apache.org

Update the file `airflow-values.yaml` attributes; repo, branch and subPath of your DAGs.

    yaml
    gitSync:
    enabled: true
    
    # git repo clone url
    # ssh examples ssh://git@github.com/apache/airflow.git
    # git@github.com:apache/airflow.git
    # https example: https://github.com/mmendoza17/data-bootcamp-terraforms-mmendoza
    
    repo: https://github.com/eiffela65/Airflow-Templates
    branch: main
    rev: HEAD
    depth: 1
    
    # the number of consecutive failures allowed before aborting
    maxFailures: 0
    
    # subpath within the repo where dags are located
    # should be "" if dags are at repo root
    subPath: ""

Install the airflow chart from the repository:

    helm install airflow -f airflow-values.yaml apache-airflow/airflow --namespace airflow

We can verify that our pods are up and running by executing:

    kubectl get pods -n airflow


<a id="org959018f"></a>

## Accessing to Airflow dashboard

The Helm chart shows how to connect:

    You can now access your dashboard(s) by executing the following command(s) and visiting the corresponding port at localhost in your browser:
    
    Airflow Webserver:     kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
    Flower dashboard:      kubectl port-forward svc/airflow-flower 5555:5555 --namespace airflow
    Default Webserver (Airflow UI) Login credentials:
        username: admin
        password: admin
    Default Postgres connection credentials:
        username: postgres
        password: postgres
        port: 5432
    
    You can get Fernet Key value by running the following:
    
        echo Fernet Key: $(kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)

As you can see, we need to access to the dashboard running:

    kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
    kubectl port-forward svc/airflow-flower 5555:5555 --namespace airflow


<a id="org5427e61"></a>

# Acknowledgments

This solution was based on this guide: [Provision a GKE Cluster guide](https://learn.hashicorp.com/tutorials/terraform/gke?in=terraform/kubernetes), containing Terraform configuration files to provision an GKE cluster on GCP.

