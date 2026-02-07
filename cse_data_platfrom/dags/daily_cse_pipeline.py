from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'kavindu',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='cse_daily_trade_pipeline',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',   # Runs once a day
    catchup=False                 # Don't run for past dates
) as dag:

    # Task 1: Run the Python Extraction Script
    extract_task = BashOperator(
        task_id='extract_cse_data',
        bash_command='python /opt/airflow/scripts/extract_cse.py {{ ds }}'
    )

    # Task 2: Run the Python Loading Script
    load_task = BashOperator(
        task_id='load_to_postgres',
        bash_command='python /opt/airflow/scripts/load_to_postgres.py {{ ds }}'
    )

    # Define Dependency: Extract MUST finish before Load starts
    extract_task >> load_task