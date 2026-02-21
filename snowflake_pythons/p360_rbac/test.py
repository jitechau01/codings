import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__consumer_con import _conn
bbt = _conn('bbt_user')
silc = _conn('silc_user')


# result=bbt.execute("""select GOV_APPROVED_PHASE_1_POS,GOV_APPROVED_PHASE_2A_POS,GOV_APPROVED_PHASE_2B_POS,GOV_APPROVED_PHASE_2_POS,GOV_APPROVED_PHASE_3_POS 
# from VW_PROJECT_INDICATION_FLAT Limit 1""").fetchall()
# for row in result:
#     print(result)
    
result=silc.execute("""select project_category,GOV_APPROVED_PHASE_1_POS,GOV_APPROVED_PHASE_2A_POS,GOV_APPROVED_PHASE_2B_POS,GOV_APPROVED_PHASE_2_POS,GOV_APPROVED_PHASE_3_POS 
from VW_PROJECT_INDICATION_FLAT Limit 1""").fetchall()
for row in result:
    print(result)
