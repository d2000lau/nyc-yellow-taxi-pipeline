from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="nyc_taxi_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["nyc-taxi"],
) as dag:

    ingest_data = BashOperator(
        task_id="ingest_data",
        bash_command="cd /opt/airflow/project && python src/ingest.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "cd /opt/airflow/project/dbt "
            "&& dbt run --profiles-dir ."
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "cd /opt/airflow/project/dbt "
            "&& dbt test --profiles-dir ."
        ),
    )

    ingest_data >> dbt_run >> dbt_test