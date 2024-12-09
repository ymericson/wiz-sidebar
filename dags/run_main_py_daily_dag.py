from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'run_main_py_daily',
    default_args=default_args,
    description='Run main.py every day at midnight',
    schedule_interval='0 0 * * *',
)

# Define the task
run_main_py = BashOperator(
    task_id='run_main_py',
    bash_command='python main.py',
    dag=dag,
)

# Set the task dependencies (if any)
run_main_py