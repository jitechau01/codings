from __con import _conn

cur=_conn()
csv_file_format_name='ff_csv'
json_file_format_name='ff_json'
parquet_file_format_name='ff_parquet'
csv_stage_name='s3_csv'
json_stage_name='s3_json'
parquet_stage_name='s3_parquet'
integration_name='s3_int'
csv_path='s3://salesinputsource/csv/'   
json_path='s3://salesinputsource/json/'   
parquet_path='s3://salesinputsource/parquet/'

def create_db_schemas():
    # cur.execute("drop database if exists working")  #uncomment this if want to recreate database
    # cur.execute("create database if not exists sales")
    # print("Database 'sales' created successfully.")
    # cur.execute("create schema if not exists sales.staging")
    # print("Schema 'sales.staging' created successfully.")
    # cur.execute("create schema if not exists sales.intermediate")
    # print("Schema 'sales.intermediate' created successfully.")
    # cur.execute("create schema if not exists sales.marts")
    # print("Schema 'sales.marts' created successfully.")
    cur.execute("use schema working.landing") 
    # print("Using schema 'sales.staging' for subsequent operations.")
    #cur.execute("drop schema if exists working.staging")  #use this if want to recreate schema
    #cur.execute("drop schema if exists working.intermediate") #use this if want to recreate schema
    #cur.execute("drop schema if exists working.marts") #use this if want to recreate schema

def create_file_formats():
    sql = f"""
    create file format if not exists {csv_file_format_name}
    type = 'csv'
    field_delimiter = ','
    skip_header = 1
    field_optionally_enclosed_by = '"'
    null_if = ('null', 'null');
    """
    cur.execute(sql)
    print(f"file format '{csv_file_format_name}' created successfully.")    

    sql = f"""
    create file format if not exists {json_file_format_name}
    type = 'json'
    strip_outer_array = true;
    """
    cur.execute(sql)
    print(f"file format '{json_file_format_name}' created successfully.")    

    sql = f"""
    create file format if not exists {parquet_file_format_name}
    type = 'parquet';
    """
    cur.execute(sql)
    print(f"file format '{parquet_file_format_name}' created successfully.")    
    
def create_stage(stage_name, file_format_name, integration_name, path):
    sql = f"""
    create stage if not exists {stage_name}
    url = '{path}' 
    file_format = {file_format_name}
    storage_integration = {integration_name};
    """
    cur.execute(sql)
    print(f"stage '{stage_name}' created successfully.")

create_db_schemas()    
create_file_formats()
create_stage(csv_stage_name, csv_file_format_name, integration_name, csv_path)
create_stage(json_stage_name, json_file_format_name, integration_name, json_path)
create_stage(parquet_stage_name, parquet_file_format_name, integration_name, parquet_path)