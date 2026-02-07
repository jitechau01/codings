import snowflake.connector
from __con import _conn
import re

cur = _conn()

integration_name='s3_int'
iam_role_arn='arn:aws:iam::108782091836:role/snowflake_s3_role'
bucket_name='salesinputsource'
path='s3://salesinputsource/'

def create_storage_integration(integration_name, iam_role_arn, bucket_name, path):
    sql = f"""
    create storage integration if not exists {integration_name}
      type = external_stage
      storage_provider = 's3'
      enabled = true
      storage_aws_role_arn = '{iam_role_arn}'
      storage_allowed_locations = ('s3://{bucket_name}/{path}/', 's3://{bucket_name}/{path}_2/');
    """
    try:
        cur.execute(sql)
        print(f"Object {integration_name} created successfully.")
    except snowflake.connector.errors.ProgrammingError as e:
        error_message = e.msg
        sql_error_code = e.sfqid
    
    if "already exists" in error_message or "002002" in error_message or "093202" in error_message:
        print(f"Info: Object {integration_name} already exists. Proceeding without creation.")
    else:
        # Re-raise the exception if it's a different error
        print(f"An unexpected error occurred: {error_message}")
        raise e
    
create_storage_integration(integration_name, iam_role_arn, bucket_name, path)
