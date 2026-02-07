from __con import _conn
cur = _conn()


cur.execute("SELECT current_version()")
one_row = cur.fetchone()
print(one_row[0])