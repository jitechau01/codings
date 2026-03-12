from airflow import DAG
from airflow.operators.python import PythonOperator 
from airflow.models import Variable
import snowflake.connector
import pandas as pd
import os

database = "RNDCONTROLLING"
tag_schema = "data_governance"
data_schema='DP_RDPORTFOLIO360'
TAG_NAME = "SENSITIVITY_LEVEL"
file=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/source_files/csv/consumer_input_files/data_classification.xlsx'

dag_config=Variable.get("snowflake_conn_policy_admin", deserialize_json=True)
account=dag_config.get("account")
user=dag_config.get("user") 
password=Variable.get("__password") 
role=dag_config.get("role")
warehouse=dag_config.get("warehouse")
database=dag_config.get("database")
schema=dag_config.get("schema")

with DAG(
    dag_id='1_dag_Create_Apply_TAGs_AND_Policies',
    schedule_interval=None,
    catchup=False
    ) as dag:
    
    def create_tags():
        conn = snowflake.connector.connect(user=user,password=password,account=account,role=role,warehouse=warehouse,database=database,schema=schema)
        cur=conn.cursor()
        try:
            print(f"""---------->creating tag {TAG_NAME} """)
            cur.execute(f"use schema {database}.{tag_schema}")
            cur.execute(f"""create tag if not exists {TAG_NAME} allowed_values 'HIGH_SENSITIVE',
                    'MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED' """)
            status=cur.fetchone()
            if status:
                message=status[0]
                if "successfully created" in message.lower():
                    print(f"Tag {TAG_NAME} created successfully")
                elif "already exists" in message.lower():
                    print(f"Tag {TAG_NAME} already exists, skipped creation")
                else:
                    print("Message:{message}")
        except Exception as e:
            print("Exception Occered: {e}")
            print("Tagging completed.") 
    def apply_tags():
        conn = snowflake.connector.connect(user=user,password=password,account=account,role=role,warehouse=warehouse,database=database,schema=schema)
        cur=conn.cursor()
        # Read Excel file
        # -----------------------------
        file_path = file
        df = pd.read_excel(file_path)

        # -----------------------------
        # Loop through rows
        # -----------------------------
        for _, row in df.iterrows():

            sensitivity_level = str(row["SENSITIVITY_LEVEL"]).strip()
            view_name = str(row["VIEW_NAME"]).strip()

            columns = str(row["COLUMN_NAME"])
            column_list = [c.strip() for c in columns.split(",") if c.strip()]

            for column in column_list:

                sql = f"""
                ALTER VIEW {database}.{data_schema}.{view_name}
                MODIFY COLUMN {column}
                SET TAG {database}.{tag_schema}.{TAG_NAME} = '{sensitivity_level}'
                """

                try:
                    print(f"Applying tag on {view_name}.{column}")
                    cur.execute(sql)
                    print(f"     tag applied successfully")
                    
                except Exception as e:
                    print(f"Error tagging {view_name}.{column}: {e}")
        print("\n\nTagging Process Completed Successfully.")       
    def create_policies():
        conn = snowflake.connector.connect(user=user,password=password,account=account,role=role,warehouse=warehouse,database=database,schema=schema)
        cur=conn.cursor()
        cur.execute(f""" use schema {database}.{tag_schema}""")
        print("\n\n\n----------->Creating String Policy")
        
        try:
            cur.execute(""" CREATE MASKING POLICY IF NOT EXISTS STRING_POLICY
            AS (VAL STRING) 
            RETURNS STRING ->
            CASE
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'LIMITED' THEN VAL
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'LOW_SENSITIVE' AND CURRENT_ROLE() IN ('LOW_ROLE','MEDIUM_ROLE','HIGH_ROLE') THEN VAL
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'MEDIUM_SENSITIVE' AND CURRENT_ROLE() IN ('MEDIUM_ROLE','HIGH_ROLE') THEN VAL
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'HIGH_SENSITIVE' AND CURRENT_ROLE() IN ('HIGH_ROLE') THEN VAL
            ELSE '**MASKED**'
            END """)
            status=cur.fetchone()
            message=status[0]
            if status:
                if "successfully created" in message.lower():
                    print("Policy created successfully")
                elif "already exists" in message.lower():
                    print("Policy Already exists, skipped creation")
                else:
                    print(message)
        except Exception as e:
            print(f"Exception occurred; {e}")
        
        print("\n\n----------->Creating Float Policy")
        try:
            cur.execute(""" CREATE MASKING POLICY IF NOT EXISTS FLOAT_POLICY
            AS (VAL FLOAT) 
            RETURNS FLOAT ->
            CASE
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'LIMITED' THEN VAL
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'LOW_SENSITIVE' AND CURRENT_ROLE() IN ('LOW_ROLE','MEDIUM_ROLE','HIGH_ROLE') THEN VAL
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'MEDIUM_SENSITIVE' AND CURRENT_ROLE() IN ('MEDIUM_ROLE','HIGH_ROLE') THEN VAL
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'HIGH_SENSITIVE' AND CURRENT_ROLE() IN ('HIGH_ROLE') THEN VAL
            ELSE -.00000000001
            END """)
            status=cur.fetchone()
            message=status[0]
            if status:
                if "successfully created" in message.lower():
                    print("Policy created successfully")
                elif "already exists" in message.lower():
                    print("Policy Already exists, skipped creation")
                else:
                    print(message)
        except Exception as e:
            print(f"Exception occurred; {e}")
        
        print("\n\n----------->Creating Number Policy")
        try:
            cur.execute(""" CREATE MASKING POLICY IF NOT EXISTS NUMBER_POLICY
            AS (VAL NUMBER) 
            RETURNS NUMBER ->
            CASE
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'LIMITED' THEN VAL
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'LOW_SENSITIVE' AND CURRENT_ROLE() IN ('LOW_ROLE','MEDIUM_ROLE','HIGH_ROLE') THEN VAL
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'MEDIUM_SENSITIVE' AND CURRENT_ROLE() IN ('MEDIUM_ROLE','HIGH_ROLE') THEN VAL
            WHEN UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('SENSITIVITY_LEVEL')) = 'HIGH_SENSITIVE' AND CURRENT_ROLE() IN ('HIGH_ROLE') THEN VAL
            ELSE -.00000000001
            END """)
            status=cur.fetchone()
            message=status[0]
            if status:
                if "successfully created" in message.lower():
                    print("Policy created successfully")
                elif "already exists" in message.lower():
                    print("Policy Already exists, skipped creation")
                else:
                    print(message)
        except Exception as e:
            print(f"Exception occurred; {e}")
    def apply_policies_to_tag():
        conn = snowflake.connector.connect(user=user,password=password,account=account,role=role,warehouse=warehouse,database=database,schema=schema)
        cur=conn.cursor()
        cur.execute(f""" use schema {database}.{tag_schema}""")
        print(f"\n\n---------->Applying Policies to tag {TAG_NAME}")
        
        cur.execute(""" alter tag SENSITIVITY_LEVEL set masking policy STRING_POLICY """)
        print("""STRING_POLICY applied to tag""")
        cur.execute(""" alter tag SENSITIVITY_LEVEL set masking policy NUMBER_POLICY """)
        print("""   NUMBER_POLICY applied to tag""")
        cur.execute(""" alter tag SENSITIVITY_LEVEL set masking policy FLOAT_POLICY """)
        print("""       FLOAT_POLICY applied to tag""")
        
    Create_Tag_Task = PythonOperator(
    task_id='Creating_Tags',
    python_callable=create_tags
)
    Apply_Tag_Task = PythonOperator(
    task_id='Applying_Tags',
    python_callable=apply_tags
)
    Create_Policies_Task = PythonOperator(
    task_id='Creating_Policies',
    python_callable=create_policies
)
    Apply_Policies_To_Task = PythonOperator(
    task_id='Applying_Policies',
    python_callable=apply_policies_to_tag
)
    Create_Tag_Task >> Apply_Tag_Task >> Create_Policies_Task >> Apply_Policies_To_Task