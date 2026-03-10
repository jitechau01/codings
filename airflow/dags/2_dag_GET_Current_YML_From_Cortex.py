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
    dag_id='2_dag_GET_Current_YML_From_Cortex',
    schedule_interval=None,
    catchup=False
    ) as dag:
    
    def Download_Current_YML():
        import snowflake.connector
        import os
        
        database = "RNDCONTROLLING"
        semantic_schema='semantic'
        semantic_stage='istage'
        stage_file_path = f"""@{database}.{semantic_schema}.{semantic_stage}/p360_Semantic_Model.yml"""
        loccal_semantic_file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/source_files/yml/'
        get_command = f"""GET {stage_file_path} file://{loccal_semantic_file_path}"""
        
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
        
        cur.execute(get_command)
        print(f"File downloaded to {loccal_semantic_file_path}")

    Sementaic_Layer_Task = PythonOperator(
        task_id='GET_Current_Cortex_YML',
        python_callable=Download_Current_YML
    )