import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from snowflake_pythons.__connections.__con_lead import _conn_lead
import os

cur=_conn_lead()

database='rndcontrolling'
rbacschema='AccessControl'
csv_file_format='ff_csv'
csv_file_format_infer='ff_csv_infer'
local_csv_stage='local_csv_stage'
csv_stage_location='@local_csv_stage/'

def create_AccessControl_schema():
    cur.execute(f"use database {database}")
    try:
        print(f"\n//Creating schema {rbacschema} in database {database}...")
        result=cur.execute(f"create schema if not exists {database}.{rbacschema}")
        status=result.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print(f"Schema {rbacschema} successfully created in database {database}")
            elif "already exists" in message.lower():
                print(f"Schema {rbacschema} already exists in database {database}, skipped creation")
                
    except Exception as e:
        print("Error:{e}")
def create_fileFormat_and_stage_objects():
    cur.execute(f"use schema {database}.{rbacschema}")
        
    try:
        print(f"\n//Creating csv file format {csv_file_format} in schema {database}.{rbacschema}...")
        result=cur.execute(f"""create file format if not exists {database}.{rbacschema}.{csv_file_format}
                            type = 'csv'
                            field_delimiter = ','
                            skip_header = 1
                            field_optionally_enclosed_by = '"'
                            null_if = ('null', 'null')""")
        status=result.fetchone()
        if status:  
            message=status[0]
            if "successfully created" in message.lower():
                print(f"file format {csv_file_format} successfully created")
            elif "already exists" in message.lower():
                print(f"file format {csv_file_format} already exists, skipped creation")
    except Exception as e:
        print(f"Error: {e}")
        
    try:
        print(f"\n//Creating csv file format {csv_file_format_infer} in schema {database}.{rbacschema}...")
        result=cur.execute(f"""create file format if not exists {database}.{rbacschema}.{csv_file_format_infer}
                            type = csv
                            field_delimiter = ','
                            parse_header = true
                            field_optionally_enclosed_by = '"'
                            null_if = ('null', 'null')""")
        status=result.fetchone()
        if status:  
            message=status[0]
            if "successfully created" in message.lower():
                print(f"file format {csv_file_format_infer} successfully created")
            elif "already exists" in message.lower():
                print(f"file format {csv_file_format_infer} already exists, skipped creation")
    except Exception as e:
        print(f"Error: {e}")
        
    try:
        print(f"\n//Creating local csv stage {local_csv_stage} in schema {database}.{rbacschema}...")
        result=cur.execute(f""" create stage if not exists {database}.{rbacschema}.{local_csv_stage} """)
        status=result.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print(f"Stage {local_csv_stage} successfully created")
            elif "already exists" in message.lower():
                print(f"Stage {local_csv_stage} already exists, skipped creation")
    except Exception as e:
        print(f"Error: {e}")   
def stage_consumer_input_files():
    try:
        cur.execute(f"use schema {database}.{rbacschema}")
        print(f"\n//Staging local csv files to {database}.{rbacschema}.{local_csv_stage}...")
        csv_local_file_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/source_files/csv/consumer_input_files'
        put_command = f"""PUT file://{csv_local_file_path}/*.csv @{database}.{rbacschema}.{local_csv_stage} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"""
        cur.execute(put_command)
        print(f"    CSV files staged successfully to @{database}.{rbacschema}.{local_csv_stage}")

    except Exception as e:
        print(f"Error: {e}")
def create_AccessControl_schema_Infered_tables():
    cur.execute(f"use schema {database}.{rbacschema}")
    try:
        print(f"\n//Creating table consumers_access in schema {database}.{rbacschema}...")
        result=cur.execute(f""" CREATE OR REPLACE TABLE consumers_access
                                USING TEMPLATE (
                                    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
                                    FROM TABLE(
                                        INFER_SCHEMA(
                                        LOCATION=>'@{local_csv_stage}',
                                        files=>'CONSUMERS_ACCESS.csv',
                                        FILE_FORMAT=>'{csv_file_format_infer}' 
                                        )
                                    )) """)
        status=result.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print("Table CONSUMER_USER_DETAILS created successfully")
            elif "already exists" in message.lower():
                print("Table CONSUMER_USER_DETAILS already exists, recreated with new schema based on staged csv file")
    except Exception as e:
        print(f"Error: {e}")
        
    try:
        print(f"\n//Creating table consumers_User_Details in schema {database}.{rbacschema}...")
        result=cur.execute(f""" CREATE OR REPLACE TABLE consumers_user_details
                                USING TEMPLATE (
                                    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
                                    FROM TABLE(
                                        INFER_SCHEMA(
                                        LOCATION=>'@{local_csv_stage}',
                                        files=>'CONSUMERS_USER_DETAILS.csv',
                                        FILE_FORMAT=>'{csv_file_format_infer}' 
                                        )
                                    )) """)
        status=result.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print("Table CONSUMER_USER_DETAILS created successfully")
            elif "already exists" in message.lower():
                print("Table CONSUMER_USER_DETAILS already exists, recreated with new schema based on staged csv file")
    except Exception as e:
        print(f"Error: {e}") 
def load_consumer_input_detail_tables():
    cur.execute(f"use schema {database}.{rbacschema}")
    print("\n//Loading consumer input details to tables...")
    table_list=['CONSUMERS_USER_DETAILS','CONSUMERS_ACCESS']
    for table in table_list:
        cur.execute(f""" truncate table {table} """)
        copy_command = f"""COPY INTO {table} FROM {csv_stage_location}{table}.csv FILE_FORMAT = (format_name = ff_csv) ON_ERROR = 'skip_file' """
        try:
            cur.execute(copy_command)
            result=cur.fetchall()
            # load_failed = False
            for row in result:
                print(f"Data loaded successfully into '{table}' ")
        
        except Exception as e:
            print("Error:{e}")          
def create_consumers_access_control_table():
    cur.execute(f"use schema {database}.{rbacschema}")
    print("\n//Creating & Populating create_consumers_access_control table")
    cur.execute(f""" create or replace table consumers_access_control as select 'bbt' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,bbt as access_type from consumers_access union all
                            select 'silc' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,silc as access_type from consumers_access union all
                            select 'accord' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,accord as access_type from consumers_access union all
                            select 'cmc' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,cmc as access_type from consumers_access union all
                            select 'cct' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,cct as access_type from consumers_access union all
                            select 'ebmo' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,ebmo as access_type from consumers_access union all
                            select 'enrich' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,enrich as access_type from consumers_access union all
                            select 'iport' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,iport as access_type from consumers_access union all
                            select 'magellan' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,magellan as access_type from consumers_access union all
                            select 'ortems' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,ortems as access_type from consumers_access union all
                            select 'eetif' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,eetif as access_type from consumers_access """)
    print(f"Table consumers_access_control created successfully with data")
create_AccessControl_schema()
create_fileFormat_and_stage_objects()
stage_consumer_input_files()
create_AccessControl_schema_Infered_tables()
load_consumer_input_detail_tables()
create_consumers_access_control_table()


