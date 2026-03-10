import os
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_lead import _conn

database='rndcontrolling'
local_csv_stage='local_csv_stage'
csv_file_format_infer='ff_csv_infer'
schema_list= ['landing','crdh_dea_iport_reporting', 'dp_rdportfolio360', 'semantic', 
              'srv_mdm_rndmasterdata', 'srv_rnd_df', 'stg_manual_inputs','data_governance']
cur=_conn()
          
def create_database():
    print("\n-------------database & schema Creation Starts-------------------")
    try:
        #cur.execute(f"DROP DATABASE IF EXISTS {database}")
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        status=cur.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print(f"Database {database} created successfully")
            else:
                print(f"Database {database} already exists")
        else:
            print(f"Failed to create database {database}")
            
    except Exception as e:
        print(f"Error creating database {database}: {e}")
def create_schemas():
    print("\n-------------Schema Creation Starts-------------------")
    for schema in schema_list:
        try:
            cur.execute(f"CREATE SCHEMA IF NOT EXISTS {database}.{schema}")
            status=cur.fetchone()
            if status:
                message=status[0]
                if "successfully created" in message.lower():
                    print(f"Schema {schema} created successfully")
                else:
                    print(f"Schema {schema} already exists")
            else:
                print(f"Failed to create schema {schema}")
                
        except Exception as e:
            print(f"Error creating schema {schema}: {e}")

create_database()
create_schemas()

    