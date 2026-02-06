from airflow import DAG
from airflow.operators.python import PythonOperator 
from airflow.models import Variable

dag_config=Variable.get("snowflake_conn", deserialize_json=True)
account=dag_config.get("account")
user=dag_config.get("user") 
password=Variable.get("__password") 
role=dag_config.get("role")
warehouse=dag_config.get("warehouse")
database=dag_config.get("database")
schema=dag_config.get("schema")

with DAG(
    dag_id='dag_snowflake_through_python',
    schedule_interval=None,
    catchup=False
    ) as dag:
    
    def test_snowflake_connection():
        import snowflake.connector
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            role=role,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        cur=conn.cursor()
        cur.execute("SELECT CURRENT_VERSION()")
        version=cur.fetchone()
        return f"Snowflake version: {version[0]}"
    
    snowflake_test_task = PythonOperator(
        task_id='test_snowflake_connection',
        python_callable=test_snowflake_connection
    )