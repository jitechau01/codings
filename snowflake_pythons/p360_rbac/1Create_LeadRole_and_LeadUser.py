import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_admin import _conn

leadRoleName=sys.argv[1]
leadUserName=sys.argv[2]
schema_list=['landing','crdh_dea_iport_reporting', 'dp_rdportfolio360', 'semantic', 'srv_mdm_rndmasterdata', 'srv_rnd_df', 'stg_manual_inputs']

def create_Leaduser_with_LeadAccess(leadRoleName,leadUserName):
    cur=_conn()
    cur.execute("drop database if exists rndcontrolling")
    cur.execute("use role securityadmin")
    
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
                cur.execute(f" alter user {leadUserName} set password='guest' ")
                print(f"Password set for user {leadUserName}")
    except Exception as e:
        print(f"Error: {e}")   
        
    cur.execute(f"alter user {leadUserName} set default_role={leadRoleName} ")
    print(f"Default role for user {leadUserName} set to {leadRoleName}")
    cur.execute(f"alter user {leadUserName} set default_warehouse='compute_wh' ")
    print(f"Default warehouse for user {leadUserName} set to 'compute_wh'")
    cur.execute(f"""alter user {leadUserName} set rsa_public_key='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo8TAWiz1Efg1HUJHqUSr
                    39UfvX2uebf3Z9vDpHhY/xwzgLYmgeDAwYIzZrSsDSRFDoPszlsgMOnrIqaI2222
                    /1XBi51+TlEqzVy43re+p62pVtBrZEISG/urjUeACto6TLqjKCzCFSetZz1y7Elj
                    fteEsDyx2+9caoRKAlSjSHBrm2S4OUO2nihdnIBz9sG1J96uuz99Si5g1QtZGAqR
                    oq1I3P290x2IriCiykKMLRI2KptYH6gkOEustEgIvDzYCBl1bXGmuw3ZG6gymlBv
                    KReLJyobBf/B8qgNJ1zKAusacNBrbMICw1OrSrLXdUT/ZRYCb5HZKdBf1cjaS/Nd
                    qQIDAQAB' """)
    print(f"RSA public key set for user {leadUserName}")
    
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
        cur.execute(f"""GRANT MANAGE GRANTS  ON ACCOUNT TO ROLE {leadRoleName}""")
        print(f"Grant MANAGE GRANTS successfully granted to role {leadRoleName}")
        
        cur.execute(f"""GRANT APPLY MASKING POLICY ON ACCOUNT TO ROLE {leadRoleName}  WITH GRANT OPTION""")
        print(f"Grant APPLY MASKING POLICY successfully granted to role {leadRoleName}")
        
        cur.execute(f"""GRANT APPLY TAG ON ACCOUNT TO ROLE {leadRoleName}  WITH GRANT OPTION""")
        print(f"Grant APPLY TAG successfully granted to role {leadRoleName}")
        
        
        
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