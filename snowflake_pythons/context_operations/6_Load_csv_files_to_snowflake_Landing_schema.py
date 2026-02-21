from snowflake_pythons.__connections.__con_lead import _conn_lead
cur=_conn_lead()

local_csv_stage='@local_csv_stage/'
database='rndcontrolling'

def load_csv_files_to_snowflake_landing_schema():
    cur.execute(f"use schema {database}.landing")
    print("\n//Loading csv files from local_csv_stage to landing tables...")
    table_list=['ICD10_MEDDRA_MAPPING', 'INDICATION', 'MDM_CLINICAL_INDICATION', 
                'MDM_FINANCIAL_ORGANIZATION_UNIT', 'MDM_PROJECT_IND_MASTER', 'MDM_PROJECT_MASTER', 
                'MEDDRA_SNOMED_CT_MAPPING', 'PHASE', 'PROJECT', 'PROJECT_TYPE', 
                'PRTFL_TCP_PROFILE', 'PRTFL_TPP_PROFILE', 'PRTFL_TVP_PROFILE', 'REF_BASELINE', 
                'RESOURCE', 'TASK', 'TEAM_MEMBER', 'WBS_HIERARCHY']
    for table in table_list:
        cur.execute(f""" truncate table {table} """)
        copy_command = f"""COPY INTO {table} FROM {local_csv_stage}{table}.csv FILE_FORMAT = (format_name = ff_csv) ON_ERROR = 'skip_file' """
        try:
            cur.execute(copy_command)
            result=cur.fetchall()
            load_failed = False
            for row in result:
                print(f"Data loaded successfully into '{table}' from local_csv_stage.")
        
        except Exception as e:
            print("Error:{e}")
            
        
        
load_csv_files_to_snowflake_landing_schema()