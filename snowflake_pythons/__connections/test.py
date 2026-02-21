from __consumer_con import _conn

cur=_conn('silc_user')

print(cur.execute("select current_version()").fetchall())