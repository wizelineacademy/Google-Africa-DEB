"""Database Ingestion Workflow

Based on: https://github.com/enroliv/adios/blob/main/dags/ingest_to_db_from_gcs.py

Description: Ingests the data from a GCS bucket into a postgres table.
"""

from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.sql import BranchSQLOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
import os

# General constants
DAG_ID = "ingestion_workflow_gcp_to_postgres"
STABILITY_STATE = "unstable"
CLOUD_PROVIDER = "gcp"

# GCP constants
GCP_CONN_ID = "google_cloud_default"
GCS_BUCKET_NAME = "africa-deb-bucket-second"
GCS_KEY_NAME = "chart-data.csv"

# Postgres constants
POSTGRES_CONN_ID = "google-demo-session-6-conn"
POSTGRES_TABLE_NAME = "chart_data"


def ingest_data_from_gcs(
    gcs_bucket: str,
    gcs_object: str,
    postgres_table: str,
    gcp_conn_id: str = "google_cloud_default",
    postgres_conn_id: str = "google-demo-session-6-conn",
):
    """Ingest data from an GCS location into a postgres table.

    Args:
        gcs_bucket (str): Name of the bucket.
        gcs_object (str): Name of the object.
        postgres_table (str): Name of the postgres table.
        gcp_conn_id (str): Name of the Google Cloud connection ID.
        postgres_conn_id (str): Name of the postgres connection ID.
    """
    import tempfile

    gcs_hook = GCSHook(gcp_conn_id=gcp_conn_id)
    psql_hook = PostgresHook(postgres_conn_id)

    with tempfile.NamedTemporaryFile() as tmp:
        gcs_hook.download(
            bucket_name=gcs_bucket, object_name=gcs_object, filename=tmp.name
        )
        psql_hook.bulk_load(table=postgres_table, tmp_file=tmp.name)


with DAG(
    dag_id=DAG_ID,
    schedule_interval="@once",
    start_date=days_ago(1),
    tags=[CLOUD_PROVIDER, STABILITY_STATE],
) as dag:
    start_workflow = DummyOperator(task_id="start_workflow")

    verify_key_existence = GCSObjectExistenceSensor(
        task_id="verify_key_existence",
        google_cloud_conn_id=GCP_CONN_ID,
        bucket=GCS_BUCKET_NAME,
        object=GCS_KEY_NAME,
    )

    create_table_entity = PostgresOperator(
        task_id="create_table_entity",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"""
            CREATE TABLE IF NOT EXISTS {POSTGRES_TABLE_NAME} (
                month VARCHAR(10),
                position INTEGER,
                artist VARCHAR(100),
                song VARCHAR(100),
                indicative_revenue NUMERIC,
                us INTEGER,
                uk INTEGER,
                de INTEGER,
                fr INTEGER,
                ca INTEGER,
                au INTEGER
            )
        """,
    )

    clear_table = PostgresOperator(
        task_id="clear_table",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"DELETE FROM {POSTGRES_TABLE_NAME}",
    )
    continue_process = DummyOperator(task_id="continue_process")

    ingest_data = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data_from_gcs,
        op_kwargs={
            "gcp_conn_id": GCP_CONN_ID,
            "postgres_conn_id": POSTGRES_CONN_ID,
            "gcs_bucket": GCS_BUCKET_NAME,
            "gcs_object": GCS_KEY_NAME,
            "postgres_table": POSTGRES_TABLE_NAME,
        },
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    validate_data = BranchSQLOperator(
        task_id="validate_data",
        conn_id=POSTGRES_CONN_ID,
        sql=f"SELECT COUNT(*) AS total_rows FROM {POSTGRES_TABLE_NAME}",
        follow_task_ids_if_false=[continue_process.task_id],
        follow_task_ids_if_true=[clear_table.task_id],
    )

    end_workflow = DummyOperator(task_id="end_workflow")

    (
        start_workflow
        >> verify_key_existence
        >> create_table_entity
        >> validate_data
    )
    validate_data >> [clear_table, continue_process] >> ingest_data
    ingest_data >> end_workflow

    dag.doc_md = __doc__