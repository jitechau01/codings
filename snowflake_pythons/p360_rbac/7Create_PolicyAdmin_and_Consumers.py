from py_compile import main
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_lead import _conn

cur=_conn()
database='rndcontrolling'
schema='dp_rdportfolio360'
policyuser='policy_user'
policyrole='policy_admin'
consumer_roles=['LIMITED_ROLE','LOW_ROLE','MEDIUM_ROLE','HIGH_ROLE']
consumer_user_list=['silcuser','radaruser','cmcuser','bbtuser','iportuser']

def create_policy_admin_role_and_user():
    print(f"\n---------->Creating role {policyrole}-----------------------")
    try:
        result=cur.execute(f"create role if not exists {policyrole}")
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "already exists" in message:
                print(f"role {policyrole} already exists, skipped creation")
            elif "successfully created" in message:
                print(f"role {policyrole} successfully created")
    except Exception as e:
        print(f"Error: {e}")

    print(f"\n---------->Creating user {policyuser}-----------------------") 
    try:
        result=cur.execute(f"create user if not exists {policyuser}")
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "already exists" in message:
                print(f"user {policyuser} already exists, skipped creation")
            elif "successfully created" in message:
                print(f"user {policyuser} successfully created")
                cur.execute(f" alter user {policyuser} set password='guest' ")
                print(f"Password set for user {policyuser}")
                cur.execute(f""" alter user {policyuser} set rsa_public_key=
                                'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo8TAWiz1Efg1HUJHqUSr
                                39UfvX2uebf3Z9vDpHhY/xwzgLYmgeDAwYIzZrSsDSRFDoPszlsgMOnrIqaI2222
                                /1XBi51+TlEqzVy43re+p62pVtBrZEISG/urjUeACto6TLqjKCzCFSetZz1y7Elj
                                fteEsDyx2+9caoRKAlSjSHBrm2S4OUO2nihdnIBz9sG1J96uuz99Si5g1QtZGAqR
                                oq1I3P290x2IriCiykKMLRI2KptYH6gkOEustEgIvDzYCBl1bXGmuw3ZG6gymlBv
                                KReLJyobBf/B8qgNJ1zKAusacNBrbMICw1OrSrLXdUT/ZRYCb5HZKdBf1cjaS/Nd
                                qQIDAQAB' """)
                print(f"RSA_PUB_KEY set for to user {policyuser}")
                cur.execute(f" grant role {policyrole} to user {policyuser}")
                print(f"Role {policyrole} granted to user {policyuser}")
                
    except Exception as e:
        print(f"Error: {e}")
def grant_privileges_to_policy_admin():
    print(f"\n---------->Granting privileges to {policyrole}-----------------------")
    
    cur.execute(f"""grant usage on warehouse compute_wh to role {policyrole}""")
    cur.execute(f"""grant usage on database {database} to role {policyrole}""")
    cur.execute(f"""grant usage on schema {database}.data_governance to role {policyrole}""")
    cur.execute(f"""GRANT USAGE, CREATE TABLE, CREATE VIEW,CREATE FUNCTION,CREATE PROCEDURE ON SCHEMA rndcontrolling.data_governance TO ROLE {policyrole} """)
    cur.execute(f"""GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE  ON ALL TABLES IN SCHEMA rndcontrolling.data_governance TO ROLE {policyrole} """)
    cur.execute(f"""GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON FUTURE TABLES IN SCHEMA rndcontrolling.data_governance TO ROLE {policyrole} """)
    cur.execute(f"""grant create tag on schema {database}.data_governance to role {policyrole}""")
    cur.execute(f"""grant apply tag on account to role {policyrole}""")
    cur.execute(f"""grant create masking policy on schema {database}.data_governance to role {policyrole}""")
    cur.execute(f"""grant usage on schema {database}.dp_rdportfolio360 to role {policyrole}""")
    cur.execute(f"""grant apply masking policy on account to role {policyrole}""")       
def create_consumer_roles_and_users():
    print(f"\n---------->Creating Consumer Roles-----------------------")
    try:
        for role in consumer_roles:
            cur.execute(f"create role if not exists {role}")
            status=cur.fetchone()
            if status:
                message=status[0]
                message=message.lower()
                if "already exists" in message:
                    print(f"role {role} already exists, skipped creation")
                elif "successfully created" in message:
                    print(f"role {role} successfully created")
    except Exception as e:
        print(f"Error creating role {role}: {e}")

    print(f"\n---------->Creating Consumer users-----------------------")
    for consumer_user in consumer_user_list:
        try:
            result=cur.execute(f"create user if not exists {consumer_user}")
            status=result.fetchone()
            if status:
                message=status[0]
                message=message.lower()
                if "already exists" in message:
                    print(f"user {consumer_user} already exists, skipped creation")
                elif "successfully created" in message:
                    print(f"user {consumer_user} successfully created")
                    cur.execute(f" alter user {consumer_user} set password='guest' ")
                    print(f"Password set for user {consumer_user}")
                    cur.execute(f""" alter user {consumer_user} set rsa_public_key=
                                    'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo8TAWiz1Efg1HUJHqUSr
                                    39UfvX2uebf3Z9vDpHhY/xwzgLYmgeDAwYIzZrSsDSRFDoPszlsgMOnrIqaI2222
                                    /1XBi51+TlEqzVy43re+p62pVtBrZEISG/urjUeACto6TLqjKCzCFSetZz1y7Elj
                                    fteEsDyx2+9caoRKAlSjSHBrm2S4OUO2nihdnIBz9sG1J96uuz99Si5g1QtZGAqR
                                    oq1I3P290x2IriCiykKMLRI2KptYH6gkOEustEgIvDzYCBl1bXGmuw3ZG6gymlBv
                                    KReLJyobBf/B8qgNJ1zKAusacNBrbMICw1OrSrLXdUT/ZRYCb5HZKdBf1cjaS/Nd
                                    qQIDAQAB' """)
        except Exception as e:
            print(f"Error: {e}")
def grant_consumer_roles_to_users():
    print()
    print(f"\n---------->Granting consumer roles to users ")
    for role in consumer_roles:
        for user in consumer_user_list:
            try:
                if role=='LIMITED_ROLE' and user=='silcuser':
                    cur.execute(f"grant role {role} to user {user}")
                if role=='LOW_ROLE' and user=='radaruser':
                    cur.execute(f"grant role {role} to user {user}")
                if role=='MEDIUM_ROLE' and user=='cmcuser':
                    cur.execute(f"grant role {role} to user {user}")
                if role=='HIGH_ROLE' and user in ('bbtuser','iportuser'):
                    cur.execute(f"grant role {role} to user {user}")
            except Exception as e:
                print(f"Error granting role {role} to user {user}: {e}")
                
    print(f"\n---------->Creating Consumer roles Hierarchy ")
    cur.execute(""" grant role LIMITED_ROLE to role LOW_ROLE """)
    print("LIMITED_ROLE Granted to LOW_ROLE")
    cur.execute(""" grant role LOW_ROLE to role MEDIUM_ROLE """)
    print(" LOW_ROLE Granted to MEDIUM_ROLE")
    cur.execute(""" grant role MEDIUM_ROLE to role HIGH_ROLE """)
    print("     MEDIUM_ROLE Granted to HIGH_ROLE")
    cur.execute(""" grant role HIGH_ROLE to role LEAD_ROLE """)
    print("         HIGH_ROLE Granted to LEAD_ROLE")
def grant_privilages_to_Consumer_Limited_Role():
    print("\n\n---------->Granting Privilages to role LIMITED_ROLE")
    cur.execute("""  grant usage on warehouse compute_wh to role LIMITED_ROLE""")
    cur.execute(""" grant usage on database rndcontrolling to role LIMITED_ROLE """)
    cur.execute(""" grant usage on schema rndcontrolling.dp_rdportfolio360 to role LIMITED_ROLE """)
    cur.execute(""" grant select on all views in schema  rndcontrolling.dp_rdportfolio360  to role LIMITED_ROLE """)
    cur.execute(""" grant select on  future views in schema  rndcontrolling.dp_rdportfolio360  to role LIMITED_ROLE """)
    
    cur.execute(""" grant usage on schema rndcontrolling.semantic to role LIMITED_ROLE """)
    cur.execute(""" grant select on all semantic views in schema  rndcontrolling.semantic  to role LIMITED_ROLE """)
    cur.execute(""" grant select on  future semantic views in schema  rndcontrolling.semantic  to role LIMITED_ROLE """)
    cur.execute(""" grant select on  future semantic views in schema  rndcontrolling.semantic  to role LIMITED_ROLE """)

    cur.execute(""" GRANT READ ON STAGE rndcontrolling.semantic.istage TO ROLE LIMITED_ROLE """)

    print("Required Privilages grated to Limited_Role")
    
if __name__ == "__main__":
    # create_policy_admin_role_and_user()
    # grant_privileges_to_policy_admin()
    # create_consumer_roles_and_users()
    # grant_consumer_roles_to_users()
    grant_privilages_to_Consumer_Limited_Role()
    