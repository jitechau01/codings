import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from snowflake_pythons.__connections.__con_lead import _conn_lead

cur=_conn_lead()
database='rndcontrolling'
consumer_role='data_consumer'
rbacschema='datasecurity'
p360_schema='DP_RDPORTFOLIO360'

cur.execute(f" use schema {database}.{rbacschema}")
result=cur.execute(f" select user_name from CONSUMER_USER_DETAILS").fetchall()
list_result= [row[0] for row in result]

def create_data_consumer_role():
    try:
        print(f"""creating Role {consumer_role} if it does not exist""")
        result=cur.execute(f"""create role if not exists {consumer_role}""")
        status=result.fetchone()
        if status:
            message=status[0]
            if "successfully created" in message.lower():
                print(f"""Role {consumer_role}" created successfully""")
            elif "already exists" in message.lower():
                print(f""" Role {consumer_role} exists, skipped creation""")
    except Exception as e:
        print(f"Error: {e}") 
def create_consumer_users():
    try:
        for value in list_result:
            print(f"""\n----creating user {value} if it does not exist""")
            result=cur.execute(f"""create user if not exists {value}""")
            status=result.fetchone()
            if status:
                message=status[0]
                if "successfully created" in message.lower():
                    print(f"""user {value}" created successfully""")
                elif "already exists" in message.lower():
                    print(f""" user {value} exists, skipped creation""")
    except Exception as e:
        print(f"Error: {e}")         
def Grant_Consumer_Role_To_Users():
    try:
        for value in list_result:
            print(f"""\n-->Granting Role {consumer_role} to user {value} """)
            cur.execute(f"show grants to user {value}")
            grants_list=cur.fetchall()
            if grants_list:
                for grant in grants_list:
                    print(f"{grant[3]} grant already exists on user, skipped granting")
            else:
                cur.execute(f"grant role {consumer_role} to user {value}")
                print(f"Role {consumer_role} granted to user {value}")
    except Exception as e:
        print(f"Eception {e} occurred ")   
def Grant_Privilages_To_Role_Data_Consumer():
        print(f"""\n-->Granting Required privilages to Role {consumer_role}""")
        cur.execute(f"""grant usage on warehouse compute_wh to role {consumer_role}""")
        cur.execute(f"""grant usage on database {database} to role {consumer_role}""")
        cur.execute(f"""grant usage on schema {database}.{p360_schema} to role {consumer_role}""")
        cur.execute(f"""grant select on all views in schema {database}.{p360_schema} to role {consumer_role}""")
        print(f"""  privilages granted""")
                
# create_data_consumer_role()  
# create_consumer_users() 
# Grant_Consumer_Role_To_Users()    
Grant_Privilages_To_Role_Data_Consumer()  
       
                        
                    

