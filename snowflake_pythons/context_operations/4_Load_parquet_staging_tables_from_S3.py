from snowflake_pythons.__connections.__con import _conn
cur=_conn()

stage_name='@s3_parquet'
table_list=['orders','products','reviews','users']  
cur.execute("use schema sales.staging")

def parquet_select_query_procedure():
    sql=""" create or replace procedure parquet_select_query_procedure(table_name varchar,stage_name varchar)
                    returns varchar
                    language sql
                    as
                    begin
                    desc table IDENTIFIER(:table_name);
                    LET res RESULTSET := (SELECT "name" as column_name,"type" as data_type from Table(result_scan(last_query_id())));
                    LET c1 CURSOR FOR res;
                    let record_value := '';
                    for record  in c1 do
                    record_value := record_value||','||'$1'||':'||record.column_name||'::'||record.data_type||' as '||record.column_name;
                    end for;
                    record_value := 'select '||Right(record_value,length(record_value)-1)||' from '||:stage_name||'/'||:table_name||'.parquet';
                    return record_value;
                    end """
    cur.execute(sql)

def load_parquet_staging_tables_from_s3():
    for table in table_list:
        cur.execute(f""" truncate table {table} """)
        select_query=cur.execute(f"""call parquet_select_query_procedure('{table}','{stage_name}')""").fetchall()[0][0]
        select_query_lower=select_query.lower()
        cur.execute(f""" create or replace table {table} as {select_query_lower} """) 
        print(f"Data loaded successfully into '{table}' from S3 parquet file.")
                
parquet_select_query_procedure()
load_parquet_staging_tables_from_s3()