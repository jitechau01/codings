from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

with DAG(
    dag_id='dag_snowflake_through_airflow',
    schedule_interval=None,
    catchup=False
    ) as dag:
    
    snowflake_test_task = SnowflakeOperator(
        task_id='test_snowflake_connection',
        sql="""use schema working.DP_RDPORTFOLIO360;
        create or replace table test_airflow_snowflake as select current_version() as version;""",
        snowflake_conn_id='snowflake_conn_id',
        )