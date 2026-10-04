from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def start_pipeline():
    print("JobPulse pipeline started successfully.")


with DAG(
    dag_id="jobpulse_pipeline",
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    tags=["jobpulse", "data-engineering"],
) as dag:

    start = PythonOperator(
        task_id="start_pipeline",
        python_callable=start_pipeline,
    )