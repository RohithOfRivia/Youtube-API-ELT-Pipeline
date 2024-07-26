from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 22, 4, 30, 0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

elt_script_dag = DAG(
    default_args=default_args,
    dag_id="elt_script_dag",
    schedule_interval="@daily",
)

def test_airflow_dag():
    print("Hello world")

test_script = PythonOperator(
    task_id='test',
    python_callable=test_airflow_dag,
    dag=elt_script_dag,
)

run_elt_script = BashOperator(
    task_id='run_elt_script',
    bash_command='python /opt/airflow/scripts/elt_script.py',
    dag=elt_script_dag,
)

run_dbt = DockerOperator(
    task_id='run_dbt',
    image='ghcr.io/dbt-labs/dbt-postgres:1.8.2',
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt"
      ],
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    mounts=[
        Mount(source='--- Replace this string with path to dbt folder in project directory ---',
              target='/dbt', type='bind'),
        
        Mount(source='--- Replace this string with path to .dbt file in dbt profiles ---',
              target='/root', type='bind')
    ],
    dag=elt_script_dag
    )


test_script >> run_elt_script >> run_dbt