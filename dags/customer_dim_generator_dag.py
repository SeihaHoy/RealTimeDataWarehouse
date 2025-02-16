import random
import pendulum
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from scripts.customer_dim_generator import generate_customer_dim_data

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


with DAG('customer_dim_generator',
    default_args=default_args,
    description='A DAG to generate large customer dimension data',
    schedule_interval=timedelta(days=1),
    start_date=start_date,
    tags=['dimension']) as dag:
    start = EmptyOperator(
        task_id='start_task',
    )

    generate_customer_dim_data = PythonOperator(
        task_id='generate_customer_dim_data',
        python_callable=generate_customer_dim_data
    )

    end = EmptyOperator(
        task_id='end_task',
    )

    start >> generate_customer_dim_data >> end
