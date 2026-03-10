from py_compile import main
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_policy_admin import _conn

cur=_conn()
cur.execute("use schema rndcontrolling.data_governance")

def Removing_Policies_From_Tags():
    policies=['FLOAT_POLICY','NUMBER_POLICY','STRING_POLICY']      
    for policy in policies:
        print("\n---------->Removing ", policy, " from Tags")
        cur.execute("""show tags in schema rndcontrolling.data_governance""")
        status=cur.fetchall()
        if status:
            for tag in status:
                try:
                    cur.execute("""alter tag rndcontrolling.data_governance.""" + tag[1] + """ unset masking policy rndcontrolling.data_governance.""" + policy)
                    result=cur.fetchone()
                    status=result[0]
                    if status:
                        if "executed successfully" in status.lower():
                            print(" " + policy + " removed from tag ", tag[1], " successfully")
                        else:                 
                            print(" Unexpected result while removing " + policy + " from tag ", tag[1], ": ", status)
                except Exception as e:
                    print(" Error removing masking policy from tag ", tag[1], ": ", e)
def drop_masking_policies():
    cur.execute("""use schema rndcontrolling.data_governance""")
    print("\n---------->Dropping Masking Policies in rndcontrolling.data_governance schema if exists any")
    cur.execute("""show masking policies""")
    policies=cur.fetchall()
    if policies:
        for policy in policies:
            try:
                cur.execute("""drop masking policy rndcontrolling.data_governance.""" + policy[1])
                result=cur.fetchone()
                status=result[0]
                if status:
                    if "successfully dropped" in status.lower():
                        print(" Masking Policy ", policy[1], " dropped successfully")
                    else:                 
                        print(" Unexpected result while dropping masking policy ", policy[1], ": ", status)
            except Exception as e:
                print(" Error dropping masking policy ", policy[1], ": ", e)
def drop_tags():
    cur.execute("""use schema rndcontrolling.data_governance""")
    print("\n---------->Dropping Tags in rndcontrolling.data_governance schema if exists any")
    cur.execute("""show tags""")
    tags=cur.fetchall()
    if tags:
        for tag in tags:
            try:
                cur.execute("""drop tag rndcontrolling.data_governance.""" + tag[1])
                result=cur.fetchone()
                status=result[0]
                if status:
                    if "successfully dropped" in status.lower():
                        print(" Tag ", tag[1], " dropped successfully")
                    else:                 
                        print(" Unexpected result while dropping tag ", tag[1], ": ", status)
            except Exception as e:
                print(" Error dropping tag ", tag[1], ": ", e)
if __name__=="__main__":
    Removing_Policies_From_Tags()
    drop_masking_policies()
    drop_tags()


