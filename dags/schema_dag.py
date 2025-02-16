import random
import pendulum
from datetime import datetime, timedelta
import os
import sys

import pandas as pd

sys.path.insert(1, '/opt/airflow/plugins/')
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from pinot_schema_operator import PinotSchemaSubmitOperator

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

with DAG('schema_dag',
         default_args=default_args,
         description='A DAG to submit all schema in a folder to Apache Pinot',
         schedule_interval=timedelta(days=1),
         start_date=start_date,
         tags=['schema']) as dag:

    start = EmptyOperator(
        task_id='start_task'
    )

    submit_schema = PinotSchemaSubmitOperator(
        task_id='submit_schemas',
        folder_path='/opt/airflow/dags/schemas',
        pinot_url='http://pinot-controller:9000/schemas'
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> submit_schema >> end