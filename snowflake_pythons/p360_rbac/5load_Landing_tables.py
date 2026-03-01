import os
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_data_engineer import _conn

cur=_conn()

local_csv_stage='@local_csv_stage/'
database='rndcontrolling'

def load_csv_files_to_snowflake_landing_schema():
    cur.execute(f"use schema {database}.landing")
    print("\n//Loading csv files from local_csv_stage to landing tables...")
    cur.execute("show tables")
    tables=cur.fetchall()
    table_list=[table[1] for table in tables]
    for table in table_list:
        cur.execute(f""" truncate table {table} """)
        print(f"\n//Loading file '{table}.csv' into table '{table}'..." )
        copy_command = f"""COPY INTO {table} FROM {local_csv_stage}{table}.csv FILE_FORMAT = (format_name = ff_csv) ON_ERROR = 'skip_file' """
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
            
load_csv_files_to_snowflake_landing_schema() 