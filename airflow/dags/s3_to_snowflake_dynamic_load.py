from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator

# Define your Snowflake and S3 details
SNOWFLAKE_CONN_ID = 'snowflake_conn_id'
AWS_CONN_ID = 'aws_conn_id'
S3_BUCKET = 'salesinputsource'
S3_PREFIX = 'parquet/' # Folder path in S3
SNOWFLAKE_STAGE = 's3_parquet'
SNOWFLAKE_TABLE = 'orders'
SNOWFLAKE_FILE_FORMAT = 'ff_parquet'

def list_s3_files_callable(**context):
    s3_hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    files = s3_hook.list_keys(bucket_name=S3_BUCKET, prefix=S3_PREFIX)
    parquet_files = [f for f in files if f.endswith('.parquet')]
    return parquet_files

with DAG(
    dag_id='s3_to_snowflake_dynamic_load',
    description='A DAG to load multiple S3 parquet files into Snowflake using dynamic task mapping',
    schedule_interval=None,
    catchup=False,
) as dag:

    list_files = PythonOperator(
        task_id='list_s3_files',
        python_callable=list_s3_files_callable,
    )