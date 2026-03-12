from airflow import DAG
from airflow.operators.python import PythonOperator 
from airflow.models import Variable

dag_config=Variable.get("snowflake_conn_dev", deserialize_json=True)
account=dag_config.get("account")
user=dag_config.get("user") 
password=Variable.get("__password") 
role=dag_config.get("role")
warehouse=dag_config.get("warehouse")
database=dag_config.get("database")
schema=dag_config.get("schema")

with DAG(
    dag_id='4_dag_PUSH_Updated_YML_To_Cortex',
    schedule_interval=None,
    catchup=False
    ) as dag:
    
    def PUSH_Updated_YML_To_Cortex():
        import snowflake.connector
        import os
        from  verified_queries import verified_queries
        import yaml
        
        database = "RNDCONTROLLING"
        schema = "DP_RDPORTFOLIO360"
        semantic_schema='semantic'
        semantic_stage='istage'
        Yml_file_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/source_files/yml'
        
        
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


        def Stage_Semantic_File():
            try:
                print(f"\n//Staging Semantic YML file {database}.{semantic_schema}.{semantic_stage}...")
                put_command = f"""PUT file://{Yml_file_path}/*.yml @{database}.{semantic_schema}.{semantic_stage} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"""
                cur.execute(put_command)
                print(f"    Semantic Model File staged successfully to @{database}.{semantic_schema}.{semantic_stage}")

            except Exception as e:
                print(f"Error: {e}")

        Stage_Semantic_File()
    
    Sementaic_Layer_Task = PythonOperator(
        task_id='Push_Updated_YML_To_Cortex',
        python_callable=PUSH_Updated_YML_To_Cortex
    )