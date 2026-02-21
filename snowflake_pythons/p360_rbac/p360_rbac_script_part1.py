from snowflake_pythons.__connections.__con_lead import _conn_lead
import os

cur=_conn_lead()

database='rndcontrolling'
csv_stage_location='@local_csv_stage/'

def create_datasecurity_schema():
    cur.execute(f"use database {database}")
    cur.execute(f"create schema if not exists {database}.datasecurity")
def create_datasecurity_schema_objects():
    cur.execute(f"use schema {database}.datasecurity")
    try:
        result=cur.execute(f"""create table if not exists consumers_access
                            (
                            Database_name string,
                            Schema_Name string,
                            Table_Name string,
                            Column_Name string,
                            DataType string,
                            bbt string,
                            silc string,
                            accord string,
                            cmc string,
                            cct string,
                            ebmo string,
                            enrich string,
                            iport string,
                            magellan string,
                            ortems string,
                            eetif string
                            )""")
        status=result.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print("table consumers_access successfully created")
            elif "already exists" in message.lower():
                print("table consumers_access already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        
    try:
        result=cur.execute("""create table if not exists datasecurity.consumer_user_details
                                (
                                consumer_name string,
                                user_name string
                                )""")
        status=result.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print("table consumer_user_details successfully created")
            elif "already exists" in message.lower():
                print("table consumer_user_details already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        
    try:
        result=cur.execute("""create file format if not exists ff_csv
                            type = 'csv'
                            field_delimiter = ','
                            skip_header = 1
                            field_optionally_enclosed_by = '"'
                            null_if = ('null', 'null')""")
        status=result.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print("file format ff_csv successfully created")
            elif "already exists" in message.lower():
                print("file format ff_csv already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        
    try:
        result=cur.execute(""" create stage if not exists local_csv_stage """)
        status=result.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print("Stage local_csv_stage successfully created")
            elif "already exists" in message.lower():
                print("Stage local_csv_stage already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")      
def stage_consumer_input_files():
    cur.execute(f"use schema {database}.datasecurity")
    print("\n//Staging local csv files to local_csv_stage...")
    csv_local_file_path=os.path.dirname(os.path.dirname((__file__)))+'/source_files/csv/consumer_input_files'
    put_command = f"PUT file://{csv_local_file_path}/*.csv {csv_stage_location} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
    cur.execute(put_command)
def load_consumer_input_detail_tables():
    cur.execute(f"use schema {database}.datasecurity")
    print("\n//Loading consumer input details to tables...")
    table_list=['CONSUMER_USER_DETAILS','CONSUMERS_ACCESS']
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
    cur.execute(f"use schema {database}.datasecurity")
    print("\n//Creating & Populating create_consumers_access_control table")
    cur.execute(f""" create or replace table {database}.datasecurity.consumers_access_control as
                        (select 'bbt' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(bbt)='BLOCK' union all
                        select 'silc' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(silc)='BLOCK' union all
                        select 'accord' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(accord)='BLOCK' union all
                        select 'cmc' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(cmc)='BLOCK' union all
                        select 'cct' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(cct)='BLOCK' union all
                        select 'ebmo' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(ebmo)='BLOCK' union all
                        select 'enrich' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(enrich)='BLOCK' union all
                        select'iport' as consumer_name, Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(iport)='BLOCK' union all
                        select 'magellan' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(magellan)='BLOCK' union all
                        select 'ortems' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(ortems)='BLOCK' union all
                        select 'eetif' as consumer_name,Database_name ,Schema_Name ,Table_Name ,Column_Name ,DataType,'masked' as access_type from consumers_access where upper(eetif)='BLOCK'); """)

create_datasecurity_schema()
create_datasecurity_schema_objects()
stage_consumer_input_files()
load_consumer_input_detail_tables()
create_consumers_access_control_table()


