import snowflake.connector as sf
import os

def _conn():
    conn=sf.connect(
        account=os.getenv('c_account'),
        user=os.getenv('c_user'),
        private_key_file=os.getenv('private_key_file_path'),
        private_key_file_pwd=os.getenv('privatekey'),
        role=os.getenv('c_role'),
        warehouse=os.getenv('c_warehouse'),
        database=os.getenv('c_database'),
        schema=os.getenv('c_schema'),
        )
    return conn.cursor()

cur=_conn()
print(cur.execute("select current_version()").fetchall())