import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_lead import _conn

cur=_conn()

database='rndcontrolling'
dev_role='Data_Engineer'
userName='Dev_User'
schema_list=['landing','crdh_dea_iport_reporting', 'dp_rdportfolio360', 'semantic', 'srv_mdm_rndmasterdata', 'srv_rnd_df', 'stg_manual_inputs']

def create_ProjectRole():
    print(f"\n---------->Creating role {dev_role}-----------------------")
    try:
        result=cur.execute(f"create role if not exists {dev_role}")
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "already exists" in message:
                print(f"role {dev_role} already exists, skipped creation")
            elif "successfully created" in message:
                print(f"role {dev_role} successfully created")
    except Exception as e:
        print(f"Error: {e}")
def create_ProjectUser(): 
    print(f"---------->Creating user {userName}-----------------------") 
    try:
        result=cur.execute(f"create user if not exists {userName}  password='guest' ")
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "already exists" in message:
                print(f"user {userName} already exists, skipped creation")
            elif "successfully created" in message:
                print(f"user {userName} successfully created")
    except Exception as e:
        print(f"Error: {e}")
    
    
    cur.execute(f"alter user {userName} set default_role={dev_role} ")

    print(f"Default role for user {userName} set to {dev_role}")
    cur.execute(f"alter user {userName} set default_warehouse=compute_wh ")
    print(f"Default warehouse for user {userName} set to 'compute_wh'")
    cur.execute(f"""alter user {userName} set rsa_public_key='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo8TAWiz1Efg1HUJHqUSr
39UfvX2uebf3Z9vDpHhY/xwzgLYmgeDAwYIzZrSsDSRFDoPszlsgMOnrIqaI2222
/1XBi51+TlEqzVy43re+p62pVtBrZEISG/urjUeACto6TLqjKCzCFSetZz1y7Elj
fteEsDyx2+9caoRKAlSjSHBrm2S4OUO2nihdnIBz9sG1J96uuz99Si5g1QtZGAqR
oq1I3P290x2IriCiykKMLRI2KptYH6gkOEustEgIvDzYCBl1bXGmuw3ZG6gymlBv
KReLJyobBf/B8qgNJ1zKAusacNBrbMICw1OrSrLXdUT/ZRYCb5HZKdBf1cjaS/Nd
qQIDAQAB' """)
    print(f"RSA public key set for user {userName}")
def grant_accesses_to_ProjectRole_and_ProjectUser():
    print(f"---------->Granting required privilages to role {dev_role}")
    try: 
        # Account level
        cur.execute("""GRANT USAGE, OPERATE, MONITOR ON WAREHOUSE compute_wh TO ROLE data_engineer """)
        cur.execute("""GRANT USAGE ON DATABASE rndcontrolling TO ROLE data_engineer """)
        for schema in schema_list:
        # Schema level
            cur.execute(f"""GRANT 
            USAGE, 
            CREATE TABLE, CREATE VIEW, CREATE STAGE,
            CREATE STREAM, 
            CREATE TASK, 
            CREATE PIPE,
            CREATE SEQUENCE, 
            CREATE FILE FORMAT,
            CREATE FUNCTION, 
            CREATE PROCEDURE
            ON SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # Table level (existing tables)
            cur.execute(f"""GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE  ON ALL TABLES IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # Future tables
            cur.execute(f"""GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON FUTURE TABLES IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # View level (existing views)
            cur.execute(f"""GRANT SELECT ON ALL VIEWS IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # Future views
            cur.execute(f"""GRANT SELECT ON FUTURE VIEWS IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # Stages
            cur.execute(f"""GRANT READ, WRITE ON ALL STAGES IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            cur.execute(f"""GRANT READ, WRITE ON FUTURE STAGES IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # Streams (future)
            cur.execute(f"""GRANT SELECT ON FUTURE STREAMS IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # Tasks
            cur.execute(f"""GRANT MONITOR, OPERATE ON ALL TASKS IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            cur.execute(f"""GRANT MONITOR, OPERATE ON FUTURE TASKS IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # Pipes
            # cur.execute(f"""GRANT MONITOR ON ALL PIPES IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # cur.execute(f"""GRANT OPERATE ON ALL PIPES IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            # Functions & Procedures
            cur.execute(f"""GRANT USAGE ON ALL FUNCTIONS IN SCHEMA rndcontrolling.{schema}   TO ROLE data_engineer """)
            cur.execute(f"""GRANT USAGE ON ALL PROCEDURES IN SCHEMA rndcontrolling.{schema} TO ROLE data_engineer """)
            print(f"All required privileges successfully granted to role {dev_role} for schema {schema}")
    except Exception as e:
        print(f"Error: {e}")
        
    print(f"---------->Granting role {dev_role} to user {userName}-----------------------")
    try:
        cur.execute(f"grant role {dev_role} to user {userName}")
        print(f"Role {dev_role} successfully granted to user {userName}")
    except Exception as e:
        print(f"Error: {e}")     
          
    print(f"---------->Granting role {dev_role} to Role lead_role  //Creating Role Hierarchy-----------------------")
    try:
        cur.execute(f"grant role {dev_role} to role  lead_role")
        print(f"Role {dev_role} successfully granted to role lead_role")
    except Exception as e:
        print(f"Error: {e}")
               
create_ProjectRole()
create_ProjectUser()
grant_accesses_to_ProjectRole_and_ProjectUser()