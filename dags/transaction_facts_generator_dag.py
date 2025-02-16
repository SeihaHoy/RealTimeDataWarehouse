from datetime import datetime, timedelta
import pendulum
import os
import sys

# sys.path.insert(1, os.path.join(os.path.dirname(__file__), '/opt/airflow/plugins/'))
# Add the plugins directory to the Python path
sys.path.insert(1, '/opt/airflow/plugins/')

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from kafka_operator import KafkaProduceOperator

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
    'start_date': start_date
}

with DAG(
    dag_id='transaction_facts_generator',
    default_args=default_args,
    description='Transaction fact data generator into kafka',
    schedule_interval=timedelta(days=1),
    tags=['fact_data']
) as dag:
    start = EmptyOperator(
        task_id='start_task'
    )

    generate_txn_data = KafkaProduceOperator(
        task_id='generate_txn_fact_data',
        kafka_broker='kafka_broker:9092',
        kafka_topic='transaction_facts',
        num_records=1000
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> generate_txn_data >> end