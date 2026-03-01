import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_admin import _conn

system_roles=['ACCOUNTADMIN','ORGADMIN','PUBLIC','SECURITYADMIN','SYSADMIN','USERADMIN']

def del_all_custom_roles():
    cur=_conn()
    cur.execute("show roles")
    cur.execute("""select "name" as role_name from Table(RESULT_SCAN(last_query_id()))""")
    roles=cur.fetchall()
    print(f"\nTotal Roles in the account: {len(roles)}")
    print("Checking each role if it is a system role or custom role and dropping the custom roles.")
    for role in roles:
        for x in role:
            if x in system_roles:
                print(f"{x} is a system role, can not be dropped.")
                pass
            else:
                print(f"{x} is a not system role, proceeding to drop.")
                try:
                    cur.execute(f"drop role if exists {x}")
                    status=cur.fetchone()
                    if status:
                        message=status[0]
                        if "successfully dropped" in message.lower():
                            print(f"        \nRole {x} dropped successfully.")                       
                except Exception as e:
                    print(f"""Error dropping role {x}: {e}\n""")                  
def del_all_custom_users():
    cur=_conn()
    cur.execute("show users")
    cur.execute("""select "name" as user_name from Table(RESULT_SCAN(last_query_id()))""")
    users=cur.fetchall()
    print(f"\nTotal Users in the account: {len(users)}")
    print("Checking user if it is a admin user and dropping if not.")
    for user in users:
        for x in user:
            cur.execute("select current_user()")
            current_user=cur.fetchone()[0]
            if x == current_user:
                print(f"{x} is a admin user, can not be dropped.")
                pass
            else:
                print(f"{x} is a not a admin user, proceeding to drop.")
                try:
                    cur.execute(f"drop user if exists {x}")
                    status=cur.fetchone()
                    if status:
                        message=status[0]
                        if "successfully dropped" in message.lower():
                            print(f"    User {x} dropped successfully.")                       
                except Exception as e:
                    print(f"""  Error dropping user {x}: {e}\n""")
    
if __name__=="__main__":
    del_all_custom_roles()
    del_all_custom_users()
    pass