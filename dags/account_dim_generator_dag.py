import sys
import pendulum
import os



from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG

# # Add the scripts directory to the Python path
# sys.path.insert(1, '/home/august/RealTimeDataWarehouse/RealTimeDataWarehouse/scripts')
from scripts.account_dim_generator import generate_account_dim_data

# setup
local_tz = pendulum.timezone('Asia/Bangkok')

start_date = datetime(2025, 1, 16, tzinfo=local_tz)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'backfill': False,
    'email': 'hoyseiha@gmail.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3, # retry 3 times
    'retry_delay': timedelta(minutes=5),
}

with DAG('account_dim_generator',
    default_args=default_args,
    description='Generate large account dimension data in a CSV file',
    schedule_interval=timedelta(days=1),
    start_date=start_date,
    tags=['schema'])as dag:

    start = EmptyOperator(
        task_id='start_task'
    )

    generate_account_dimension_data = PythonOperator(
        task_id='generate_account_dim_data',
        python_callable=generate_account_dim_data
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> generate_account_dimension_data >> end