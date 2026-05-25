from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "strava_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):

    etl = BashOperator(
        task_id="etl",
        bash_command="""
        docker exec etl python /app/bronze_load.py
        """
    )

    dbt = BashOperator(
        task_id="dbt",
        bash_command="""
        docker exec dbt dbt run
        """
    )

    etl >> dbt