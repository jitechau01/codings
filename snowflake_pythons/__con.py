import snowflake.connector as sf
import os

def _conn():
    conn=sf.connect(
        account=os.getenv('account'),
        user=os.getenv('user'),
        private_key_file=os.getenv('private_key_file_path'),
        private_key_file_pwd=os.getenv('privatekey'),
        role=os.getenv('role'),
        warehouse=os.getenv('_snf_warehouse'),
        database=os.getenv('_snf_database'),
        schema=os.getenv('_snf_schema'),
        )
    return conn.cursor()
