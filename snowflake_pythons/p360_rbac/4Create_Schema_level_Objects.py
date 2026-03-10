import os
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_data_engineer import _conn

cur=_conn()
database,semantic_schema,semantic_stage='rndcontrolling','semantic','istage'
local_csv_stage,csv_file_format,parquet_file_format,json_file_format='local_csv_stage','ff_csv','ff_parquet','ff_json'
csv_file_format_infer='ff_csv_infer'
schema_list= ('landing','crdh_dea_iport_reporting', 'dp_rdportfolio360', 'semantic', 
              'srv_mdm_rndmasterdata', 'srv_rnd_df', 'stg_manual_inputs')
landing,iport,p360,semantic,mdm,srv,stg=schema_list
cur.execute(f"""use schema {database}.{landing}""")
          
def create_file_format():
    print("\n//Creating ff_csv file format...")
    sql = """
    create file format if not exists ff_csv
    type = 'CSV'
    field_delimiter = ','
    skip_header = 1
    null_if = ('NULL', 'null')
    empty_field_as_null = true
    error_on_column_count_mismatch = false
    field_optionally_enclosed_by = '"'
    trim_space = true
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"file format 'ff_csv' created successfully")
            elif "already exists" in message:
                print(f"file format 'ff_csv' already exists, skipped creation")
    except Exception as e:
        print(f"""Error creating file format 'ff_csv': {e}""")
        
    print("\n//Creating ff_csv_infer file format...")
    sql = """
    create file format if not exists ff_csv_infer
    type = 'CSV'
    field_delimiter = ','
    parse_header=true
    null_if = ('NULL', 'null')
    empty_field_as_null = true
    error_on_column_count_mismatch = false
    field_optionally_enclosed_by = '"'
    trim_space = true
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"file format 'ff_csv_infer' created successfully")
            elif "already exists" in message:
                print(f"file format 'ff_csv_infer' already exists, skipped creation")
    except Exception as e:
        print(f"""Error creating file format 'ff_csv_infer': {e}""")
    
    print("\n//Creating ff_parquet file format...")    
    sql = """ create file format if not exists ff_parquet type = 'PARQUET' """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"file format 'ff_parquet' created successfully")
            elif "already exists" in message:
                print(f"file format 'ff_parquet' already exists, skipped creation")
    except Exception as e:
        print(f"Error creating file format 'ff_parquet': {e}")
    
    print("\n//Creating ff_json file format...")    
    sql = """
    create file format if not exists ff_json
    type = 'JSON'
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"file format 'ff_json' created successfully")
            elif "already exists" in message:
                print(f"file format 'ff_json' already exists, skipped creation")
    except Exception as e:
        print(f"Error creating file format 'ff_json': {e}")         
def create_local_stage():
    print("\n//Creating local stages...")
    sql = f"""
    create stage if not exists local_csv_stage
    file_format = ff_csv
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"stage 'local_csv_stage' created successfully")
            elif "already exists" in message:
                print(f"stage 'local_csv_stage' already exists. Message, skipped creation")
    except Exception as e:
        print(f"Error creating stage 'local_csv_stage': {e}")
    sql = f"""
    create stage if not exists local_parquet_stage
    file_format = ff_parquet
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"stage 'local_parquet_stage' created successfully")
            elif "already exists" in message:
                print(f"stage 'local_parquet_stage' already exists. Message, skipped creation")
    except Exception as e:
        print(f"Error creating stage 'local_parquet_stage': {e}")
    
    sql = f"""
    create stage if not exists local_json_stage
    file_format = ff_json
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"stage 'local_json_stage' created successfully")
            elif "already exists" in message:
                print(f"stage 'local_json_stage' already exists. Message, skipped creation")
    except Exception as e:
        print(f"Error creating stage 'local_json_stage': {e}")  
def stage_consumer_input_files():
    try:
        print(f"\n//Staging local csv files to {database}.{landing}.{local_csv_stage}...")
        csv_local_file_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/source_files/csv/'
        put_command = f"""PUT file://{csv_local_file_path}/*.csv @{database}.{landing}.{local_csv_stage} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"""
        cur.execute(put_command)
        print(f"    CSV files staged successfully to @{database}.{landing}.{local_csv_stage}")

    except Exception as e:
        print(f"Error: {e}")
def create_landing_schema_Infered_tables():
    cur.execute("list @local_csv_stage")
    staged_files=cur.fetchall()
    csv_file_format_infer='ff_csv_infer'
    for file in staged_files:
        filename=file[0].split('/')[-1]
        if filename.endswith('.csv'):
            table_name=filename.split('.')[0].lower()
            try:
                print(f"\n//Creating table {table_name} in schema {database}.{landing}...")
                result=cur.execute(f""" CREATE OR REPLACE TABLE {table_name}
                                        USING TEMPLATE (
                                            SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
                                            FROM TABLE(
                                                INFER_SCHEMA(
                                                LOCATION=>'@{local_csv_stage}',
                                                files=>'{filename}',
                                                FILE_FORMAT=>'{csv_file_format_infer}' 
                                                )
                                            )) """)
                status=result.fetchone()
                if status:
                    message=status[0]
                    if "successfully created" in message.lower():
                        print(f"Table {table_name} created successfully")
                    elif "already exists" in message.lower():
                        print(f"Table {table_name} already exists, recreated with new schema based on staged csv file")
            except Exception as e:
                print(f"Error: {e}")
def load_csv_files_to_snowflake_landing_schema():
    cur.execute(f"use schema {database}.landing")
    print("\n//Loading csv files from local_csv_stage to landing tables...")
    cur.execute("show tables")
    tables=cur.fetchall()
    table_list=[table[1] for table in tables]
    for table in table_list:
        cur.execute(f""" truncate table {table} """)
        print(f"\n//Loading file '{table}.csv' into table '{table}'..." )
        copy_command = f"""COPY INTO {table} FROM @{local_csv_stage}{table}.csv FILE_FORMAT = (format_name = ff_csv) ON_ERROR = 'skip_file' """
        try:
            result=cur.execute(copy_command)
            status=result.fetchone()
            if status:
                message=status[1]
                message=message.lower()
                if "loaded" in message:
                    print(f"    File '{table}.csv' loaded successfully into table '{table}'")
                elif "skipped" in message:
                    print(f"File '{table}.csv' skipped due to errors, check load history for details")
        except Exception as e:
            print(f"Error loading file '{table}.csv' into table '{table}': {e}") 
            
        cur.execute(""" alter table project_indication_flat add GOV_APPROVED_PHASE_1_POS float,GOV_APPROVED_PHASE_2A_POS float,GOV_APPROVED_PHASE_2B_POS float,GOV_APPROVED_PHASE_2_POS float,GOV_APPROVED_PHASE_3_POS float """)

        cur.execute(""" update project_indication_flat set GOV_APPROVED_PHASE_1_POS=1 ,GOV_APPROVED_PHASE_2A_POS=2 ,GOV_APPROVED_PHASE_2B_POS =3,GOV_APPROVED_PHASE_2_POS=4 ,GOV_APPROVED_PHASE_3_POS =5 """)            
def Create_Semantic_Model():
    cur.execute(f"use schema {database}.{semantic_schema}")
    print("\n\n---------->Creating semantic stage...")
    sql = f""" create stage if not exists {semantic_stage} DIRECTORY = (ENABLE = TRUE)"""
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"stage {semantic_stage} created successfully")
            elif "already exists" in message:
                print(f"stage {semantic_stage} already exists. Message, skipped creation")
    except Exception as e:
        print(f"Error creating stage {semantic_stage}: {e}")
    
# create_file_format()
# create_local_stage()
# stage_consumer_input_files()
# create_landing_schema_Infered_tables()
# load_csv_files_to_snowflake_landing_schema()
Create_Semantic_Model()