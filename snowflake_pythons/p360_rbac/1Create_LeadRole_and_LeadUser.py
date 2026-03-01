import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_admin import _conn

leadRoleName=sys.argv[1]
leadUserName=sys.argv[2]
schema_list=['landing','crdh_dea_iport_reporting', 'dp_rdportfolio360', 'semantic', 'srv_mdm_rndmasterdata', 'srv_rnd_df', 'stg_manual_inputs']

def create_Leaduser_with_LeadAccess(leadRoleName,leadUserName):
    cur=_conn()
    cur.execute("use role accountadmin")
    
    print("\n---------->Lead Role Creation Starts-----------------------")
    try:
        result=cur.execute(f"create role if not exists {leadRoleName}")
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "already exists" in message:
                print(f"role {leadRoleName} already exists, skipped creation")
            elif "successfully created" in message:
                print(f"role {leadRoleName} successfully created")
    except Exception as e:
        print(f"Error: {e}")
    
    print("---------->Lead user Creation Starts-----------------------") 
    try:
        result=cur.execute(f"create user if not exists {leadUserName}")
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "already exists" in message:
                print(f"user {leadUserName} already exists, skipped creation")
            elif "successfully created" in message:
                print(f"user {leadUserName} successfully created")
    except Exception as e:
        print(f"Error: {e}")       
def grant_accesses_to_leadrole_and_leaduser(leadRoleName):
    cur=_conn()
    print("---------->Granting required privilages to Lead role")
    try: 
        cur.execute(f"""GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE {leadRoleName}""")
        print(f"Grant USAGE ON WAREHOUSE COMPUTE_WH successfully granted to role {leadRoleName}")
        print(f"Grant CREATE DATABASE successfully granted to role {leadRoleName}")
        cur.execute(f"""GRANT CREATE DATABASE ON ACCOUNT TO ROLE {leadRoleName}""")
        print(f"Grant CREATE DATABASE successfully granted to role {leadRoleName}")
        cur.execute(f"""GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE {leadRoleName}""")
        print(f"Grant CREATE WAREHOUSE successfully granted to role {leadRoleName}")
        cur.execute(f"""GRANT CREATE ROLE      ON ACCOUNT TO ROLE {leadRoleName}""")
        print(f"Grant CREATE ROLE successfully granted to role {leadRoleName}")
        cur.execute(f"""GRANT CREATE USER      ON ACCOUNT TO ROLE {leadRoleName}""")
        print(f"Grant CREATE USER successfully granted to role {leadRoleName}")
        cur.execute(f"""GRANT MANAGE GRANTS    ON ACCOUNT TO ROLE {leadRoleName}""")
        print(f"Grant MANAGE GRANTS successfully granted to role {leadRoleName}")
        cur.execute(f"""GRANT MONITOR USAGE    ON ACCOUNT TO ROLE {leadRoleName}""")
        print(f"Grant MONITOR USAGE successfully granted to role {leadRoleName}")
        cur.execute(f"""GRANT EXECUTE TASK     ON ACCOUNT TO ROLE {leadRoleName}""")
        print(f"Grant EXECUTE TASK successfully granted to role {leadRoleName}")
        cur.execute(f"""GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE {leadRoleName}""")
        print(f"Grant CREATE INTEGRATION successfully granted to role {leadRoleName}")
        cur.execute(f"""GRANT ROLE {leadRoleName} TO ROLE SYSADMIN""")

    except Exception as e:
        print(f"Error: {e}")
        
    print("---------->Granting Lead Role to Lead user-----------------------")
    cur.execute(f"grant role {leadRoleName} to user {leadUserName}")
    print(f"Role {leadRoleName} successfully granted to user {leadUserName}")

create_Leaduser_with_LeadAccess(leadRoleName,leadUserName)
grant_accesses_to_leadrole_and_leaduser(leadRoleName)