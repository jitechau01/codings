import snowflake.connector as sf
import os

def _conn(user):
    conn=sf.connect(
        account=os.getenv('account'),
        user=user,
        private_key_file=os.getenv('private_key_file_path'),
        private_key_file_pwd=os.getenv('privatekey'),
        role='data_consumer',
        warehouse='compute_wh',
        database='rndcontrolling',
        schema='dp_rdportfolio360'
        )
    return conn.cursor()

# cur=_c_conn('bbt_user')
# print(cur.execute("select current_version()").fetchall())