import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__consumer_con import _conn

consumer_user=sys.argv[1]
cur = _conn(consumer_user)
    

if consumer_user=='cmcuser':
    cur.execute("""select PROJECT_STATUS,PROJECT_PHASE,PROJECT_PRIORITY,INDICATION_PHASE,GOV_APPROVED_PHASE_1_POS,GOV_APPROVED_PHASE_2A_POS,GOV_APPROVED_PHASE_2B_POS,GOV_APPROVED_PHASE_2_POS,GOV_APPROVED_PHASE_3_POS from VW_PROJECT_INDICATION_FLAT limit 5 """)
    bbt_df1=cur.fetch_pandas_all()
    print("\n\n")
    print(bbt_df1)
    print()
    print("**************************************************************************")
    print()
    cur.execute("""select PROJECT_TEAM_MEMBER_DESC,PROJECT_TEAM_MEMBER_SUB_TEAMS,PROJECT_TEAM_MEMBER_EMAIL from VW_PROJECT_TEAM_MEMBER limit 5 """)
    bbt_df2=cur.fetch_pandas_all()
    print(bbt_df2)

if consumer_user=='silcuser':
    cur.execute("""select project_category,GOV_APPROVED_PHASE_1_POS,GOV_APPROVED_PHASE_2A_POS,GOV_APPROVED_PHASE_2B_POS,GOV_APPROVED_PHASE_2_POS,GOV_APPROVED_PHASE_3_POS
    from VW_PROJECT_INDICATION_FLAT Limit 5 """)
    silc_df1=cur.fetch_pandas_all()
    print("\n\n")
    print()
    print(silc_df1)
    print()
    print("**************************************************************************")
    print()

if consumer_user=='radaruser':
    cur.execute("""select SANOFI_MEDDRA_INDICATION_CODE,ICD10_CODE_2019_INTL_CORE_VER,MEDDRA_PT_CODE,MEDDRA_LLT_CODE from VW_MEDDRA_ICD10_MAPPING  limit 5 """)
    radar_df1=cur.fetch_pandas_all()
    print("\n\n")
    print()
    print(radar_df1)
    print("**************************************************************************")
    cur.execute("""select INDICATION_PHASE,GOV_APPROVED_PHASE_1_POS,GOV_APPROVED_PHASE_2A_POS,GOV_APPROVED_PHASE_2B_POS,GOV_APPROVED_PHASE_2_POS,GOV_APPROVED_PHASE_3_POS from VW_PROJECT_INDICATION_FLAT  limit 5 """)
    radar_df2=cur.fetch_pandas_all()
    print()
    print(radar_df2)
    
if consumer_user=='bbtuser':
    cur.execute("""select PROJECT_CODE,PROJECT_NAME,TCP_CHARACTERISTIC_VALUE,TCP_STATUS from VW_PROJECT_TCP limit 5 """)
    bbt_df1=cur.fetch_pandas_all()
    print("\n\n")
    print(bbt_df1)
    print()
    print("**************************************************************************")
    print()
    cur.execute("""select PROJECT_CODE,INDICATION_UNIQUE_CODE,TVP_STATUS from VW_PROJECT_TVP limit 5 """)   
    bbt_df2=cur.fetch_pandas_all()
    print("\n\n")
    print(bbt_df2)
    print()
    print("**************************************************************************")
    print()

if consumer_user=='iportuser':
    cur.execute("""select INDICATION_PHASE,GOV_APPROVED_PHASE_1_POS,GOV_APPROVED_PHASE_2A_POS,GOV_APPROVED_PHASE_2B_POS,GOV_APPROVED_PHASE_2_POS,GOV_APPROVED_PHASE_3_POS 
    from VW_PROJECT_INDICATION_FLAT Limit 5 """)
    iport_df1=cur.fetch_pandas_all()
    print("\n\n")
    print()
    print(iport_df1)

