from py_compile import main
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_policy_admin import _conn

cur=_conn()
cur.execute("use schema rndcontrolling.data_governance")

def create_Float_policy():
    try:
        print("\n---------->Creating Float Type Masking Policy")
        cur.execute("""CREATE masking policy if not exists rndcontrolling.data_governance.Float_POLICY AS (val FLOAT) 
                        RETURNS FLOAT ->
                        CASE
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='BBT' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_bbt_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='SILC' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_silc_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='IPORT' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_iport_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='CMC' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_cmc_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='RADAR' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_radar_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        else NVL(VAL,0)
                        END""")
        result=cur.fetchone()
        status=result[0]
        if status:
            if "successfully created" in status.lower():
                 print("Float Type Masking Policy Created Successfully")
            elif "already exists" in status.lower():                 
                print("Float Type Masking Policy Already Exists, skipping creation")
            else:                 
                print("Unexpected result: ", status)
    except Exception as e:
        print("Error creating Float Type  Masking Policy: ", e)       
def create_Number_policy():
    try:
        print("\n---------->Creating Number Type Masking Policy")
        cur.execute("""CREATE masking policy if not exists rndcontrolling.data_governance.Number_POLICY AS (val Number) 
                        RETURNS Number ->
                        CASE
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='BBT' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_bbt_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='SILC' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_silc_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='IPORT' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_iport_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='CMC' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_cmc_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='RADAR' and 
                        UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_radar_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then -1
                        else NVL(VAL,0)
                        END""")
        result=cur.fetchone()
        status=result[0]
        if status:
            if "successfully created" in status.lower():
                 print("Number Type Masking Policy Created Successfully")
            elif "already exists" in status.lower():                 
                print("Number Type Masking Policy Already Exists, skipping creation")
            else:                 
                print("Unexpected result: ", status)
    except Exception as e:
        print("Error creating Number Type  Masking Policy: ", e)
def create_String_policy():      
    try:
            print("\n---------->Creating String Masking Policy")
            cur.execute("""CREATE masking policy if not exists rndcontrolling.data_governance.STRING_POLICY AS (val STRING) 
                            RETURNS STRING ->
                            CASE
                            WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='BBT' and 
                            UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_bbt_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then '**MASKED**'
                            WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='SILC' and 
                            UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_silc_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then '**MASKED**'
                            WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='IPORT' and 
                            UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_iport_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then '**MASKED**'
                            WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='CMC' and 
                            UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_cmc_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then '**MASKED**'
                            WHEN EXISTS (select  distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP  where upper(user_name)= upper(current_user()) and upper(ADGROUP)='RADAR' and 
                            UPPER(SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tag_radar_masked')) in ('HIGH_SENSITIVE','MEDIUM_SENSITIVE','LOW_SENSITIVE','LIMITED'))  Then '**MASKED**'
                            else NVL(VAL,'')
                            END""")
            result=cur.fetchone()
            status=result[0]
            if status:
                if "successfully created" in status.lower():
                    print("String Masking Policy Created Successfully")
                elif "already exists" in status.lower():                 
                    print("String Masking Policy Already Exists, skipping creation")
                else:                 
                    print("Unexpected result: ", status)
    except Exception as e:
        print("Error creating String Masking Policy: ", e)
def Applying_Masking_Policies_To_Tags():
    policies=['FLOAT_POLICY','NUMBER_POLICY','STRING_POLICY']      
    for policy in policies:
        print("\n---------->Applying ", policy, " to Tags")
        cur.execute("""show tags in schema rndcontrolling.data_governance""")
        status=cur.fetchall()
        if status:
            for tag in status:
                try:
                    cur.execute("""alter tag rndcontrolling.data_governance.""" + tag[1] + """ set masking policy rndcontrolling.data_governance.""" + policy)
                    result=cur.fetchone()
                    status=result[0]
                    if status:
                        if "executed successfully" in status.lower():
                            print(" " + policy + " applied to tag ", tag[1], " successfully")
                        else:                 
                            print(" Unexpected result while applying " + policy + " to tag ", tag[1], ": ", status)
                except Exception as e:
                    print(" Error applying masking policy to tag ", tag[1], ": ", e)

if __name__=="__main__":
    create_Float_policy()
    create_Number_policy()
    create_String_policy()
    Applying_Masking_Policies_To_Tags()
    


