import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__consumer_con import _conn

consumer_user=sys.argv[1]
cur = _conn(consumer_user)
    
cur.execute("""select project_category,GOV_APPROVED_PHASE_1_POS,GOV_APPROVED_PHASE_2A_POS,GOV_APPROVED_PHASE_2B_POS,GOV_APPROVED_PHASE_2_POS,GOV_APPROVED_PHASE_3_POS 
from VW_PROJECT_INDICATION_FLAT Limit 5""")

df=cur.fetch_pandas_all()
print(df)

