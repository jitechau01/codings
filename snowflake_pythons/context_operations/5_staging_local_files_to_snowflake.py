import os
from snowflake_pythons.__connections.__con_lead import _conn_lead

cur=_conn_lead()
database='rndcontrolling'

def stage_local_files():
    cur.execute(f"use schema {database}.landing")
    print("\n//Staging local csv files to local_csv_stage...")
    pqt_local_file_path=os.path.dirname(os.path.dirname((__file__)))+'/source_files/csv'
    pqt_stage_location='@local_csv_stage/'
    put_command = f"PUT file://{pqt_local_file_path}/*.csv {pqt_stage_location} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
    cur.execute(put_command)
    
stage_local_files()