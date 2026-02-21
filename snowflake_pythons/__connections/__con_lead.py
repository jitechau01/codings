import snowflake.connector as sf
import os

def _conn_lead():
    conn=sf.connect(
        account=os.getenv('account'),
        user='lead_user',
        private_key_file=os.getenv('private_key_file_path'),
        private_key_file_pwd=os.getenv('privatekey'),
        role='lead',
        warehouse='compute_wh'
        )
    return conn.cursor()

cur=_conn_lead()
print(cur.execute("select current_version()").fetchall())