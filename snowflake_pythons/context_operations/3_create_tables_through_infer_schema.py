from snowflake_pythons.__connections.__con_admin import _conn

cur=_conn()
infer_schema_file_format_name='ff_infer'
table_list=['orders','products','reviews','users']
stage_name='s3_parquet'

cur.execute("use schema sales.staging")

def infer_schema_file_format(infer_schema_file_format_name):
    sql = f"""
    create file format if not exists {infer_schema_file_format_name}
    type = 'parquet'
    """
    cur.execute(sql)
    print(f"File format '{infer_schema_file_format_name}' created successfully.")  
def create_table_through_infer_schema():
    for table in table_list:
        sql = f"""
        create or replace table {table}
        using template (select array_agg(object_construct(*))
        from table(infer_schema(
            location => '@{stage_name}/{table}.parquet',
            file_format => '{infer_schema_file_format_name}',
            ignore_case => true
            )
            )
            )
            """
        cur.execute(sql)
        print(f"Table '{table}' created successfully using inferred schema.")
    
#infer_schema_file_format(infer_schema_file_format_name)
create_table_through_infer_schema()
