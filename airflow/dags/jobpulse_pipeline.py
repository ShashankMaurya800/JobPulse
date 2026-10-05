from datetime import datetime
import subprocess

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


PROJECT_ROOT = "/opt/airflow/project"


def run_script(script_name):
    subprocess.run(
        ["python", f"{PROJECT_ROOT}/src/{script_name}"],
        check=True,
    )


with DAG(
    dag_id="jobpulse_pipeline",
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    tags=["jobpulse", "data-engineering"],
) as dag:

    ingestion = PythonOperator(
        task_id="ingestion",
        python_callable=lambda: run_script("ingestion.py"),
    )

    cleaning = PythonOperator(
        task_id="cleaning",
        python_callable=lambda: run_script("cleaning.py"),
    )

    transformation = PythonOperator(
        task_id="transformation",
        python_callable=lambda: run_script("transformation.py"),
    )

    validation = PythonOperator(
        task_id="validation",
        python_callable=lambda: run_script("validation.py"),
    )

    load = PythonOperator(
        task_id="load",
        python_callable=lambda: run_script("load_data.py"),
    )

    ingestion >> cleaning >> transformation >> validation >> load