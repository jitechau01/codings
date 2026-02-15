import snowflake.connector as sf
import os

def _conn_adam():
    conn=sf.connect(
        account=os.getenv('account'),
        user='adam',
        private_key_file=os.getenv('private_key_file_path'),
        private_key_file_pwd=os.getenv('privatekey'),
        role='lead',
        warehouse='compute_wh'
        )
    return conn.cursor()

# cur=_conn_adam()


# print(cur.execute("select current_version()").fetchall())