from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import subprocess

def run_crewai():
    subprocess.run(["python", "run.py"])

with DAG("threat_ai_pipeline",
         schedule_interval="@hourly",
         start_date=datetime(2025, 8, 1),
         catchup=False) as dag:

    run_task = PythonOperator(
        task_id="run_threat_ai",
        python_callable=run_crewai
    )