import snowflake.connector
from snowflake_pythons.__connections.__con import _conn
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
      storage_allowed_locations = ('s3://{bucket_name}/{path}/', 's3://{bucket_name}/{path}/');
    """
    cur.execute(sql)
    
    print(f"Storage integration '{integration_name}' created successfully.")   
    
create_storage_integration(integration_name, iam_role_arn, bucket_name, path)
