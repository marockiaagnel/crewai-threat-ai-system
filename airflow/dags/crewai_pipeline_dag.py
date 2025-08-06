from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from crew import ThreatAICrew

def run_crewai_pipeline():
    email_logs = ["Received: from mail.example.com (203.0.113.45)..."]
    crew = ThreatAICrew().get_crew(inputs={"logs": email_logs})
    crew.kickoff()

with DAG(
    dag_id="crewai_pipeline_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@hourly",
    catchup=False,
) as dag:
    execute_pipeline = PythonOperator(
        task_id="run_threat_detection_pipeline",
        python_callable=run_crewai_pipeline
    )