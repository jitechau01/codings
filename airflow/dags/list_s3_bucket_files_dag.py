from datetime import datetime
import logging

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator

# Initialize a logger for the task
task_logger = logging.getLogger("airflow.task")

def log_s3_files(**context):
    s3_keys = context['ti'].xcom_pull(task_ids='list_s3_keys')
    
    if s3_keys:
        task_logger.info("Found the following files in the S3 bucket:")
        for key in s3_keys:
            task_logger.info(f"* {key}")
    else:
        task_logger.info("No files found in the specified S3 bucket/prefix.")

with DAG(
    dag_id='list_s3_bucket_files_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,  # Run manually
    catchup=False,
    tags=['aws', 's3', 'list']
) as dag:
    
    # Task to list objects in an S3 bucket
    list_s3_keys = S3ListOperator(
        task_id='list_s3_keys',
        bucket='salesinputsource',  # Replace with your S3 bucket name
        prefix='parquet/',      # Optional: filter by a specific prefix/folder                # Optional: use delimiter to list only top-level files in a "folder"
        aws_conn_id='aws_conn_id'       # Reference to your Airflow AWS connection
    )

    # Python task to process and log the output
    log_files_task = PythonOperator(
        task_id='log_files_to_logs',
        python_callable=log_s3_files,
        provide_context=True  # Required to access task instance (ti) and XComs
    )

    # Define the task flow
    list_s3_keys >> log_files_task
