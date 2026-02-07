from airflow.models import DAG
from airflow.decorators import task
from datetime import datetime
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
import logging

with DAG(
    dag_id='list_s3_files_in_logs',
    schedule_interval=None,
    catchup=False,
    tags=['s3', 'list', 'aws']
) as dag:

    list_s3_files = S3ListOperator(
        task_id='list_files_in_bucket',
        bucket='salesinputsource',
        prefix='parquet/',
        delimiter='/',
        aws_conn_id='aws_conn_id',
    )

    @task(task_id="print_objects_to_logs")
    def print_objects_to_logs(object_keys):
        """Logs the list of S3 object keys."""
        logging.info("S3 Object Keys:")
        for key in object_keys:
            logging.info(key)

    print_objects_to_logs(list_s3_files.output)
