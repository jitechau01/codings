import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from snowflake_pythons.__connections.__con_lead import _conn_lead

cur=_conn_lead()
database='rndcontrolling'
schema='datasecurity'
consumer_role='data_consumer'
p360_schema='dp_rdportfolio360'
tag_name='data_sensitivity'
NumberPolicy='NUMBER_POLICY'

def create_tag_data_sensitivity():
    try:
        print("---------->Creating tag data_sensitivity")
        cur.execute(f"""CREATE tag if not exists {database}.{schema}.{tag_name} ALLOWED_VALUES 'NUMBER_MASK','STRING_MASK',
                'FLOAT_MASK','DATE_MASK','BOOLEAN_MASK' """)
        data_sensitivity=cur.fetchone()
        message=data_sensitivity[0]
        if "successfully created" in message.lower():
            print("Tag Successfully Created")
        elif "already exists" in message.lower():
            print("data_sensitivity Tag already exists, skipped creation")
    except Exception as e:
        print("Error: {e}")
def create_masking_policies():
    try:
        print(f"---------->Creating masking policy {NumberPolicy}")
        cur.execute(f" use schema {database}.{schema}")
        cur.execute(f"""create or replace masking policy NUMBER_POLICY
                    as (val float) returns float ->
                        case
                            WHEN EXISTS (
                            with cd as
                                    (select l.consumer,r.user_name,l.policy_type,l.access 
                                    from consumers_Column_Control l,consumer_user_details r 
                                    where l.consumer=r.consumer),
                                    cu as (select upper(current_user)  as current_user)
                                    select distinct cd.consumer from cd,cu
                                    where upper(cd.user_name)=cu.current_user
                                    and upper(policy_type)='NUMBER'
                                    and upper(cd.access)='MASKED'
                            )
                            THEN .00000001
                            ELSE NVL(VAL,0)
                        END """)
        masking_policy=cur.fetchone()
        message=masking_policy[0]
        if "successfully created" in message.lower():
            print("Masking Policy Successfully Created")
        elif "already exists" in message.lower():
            print("This Policy already exists, skipped creation")
    except Exception as e:
        print("Error: {e}")      
def apply_policies_to_tag():
    try:
        print(f"Applying Policy {floatpolicy} to tag {tag_name}")
        cur.execute(f"""ALTER TAG {database}.{schema}.{tag_name} SET MASKING POLICY {database}.{schema}.{floatpolicy}""")
        message=cur.fetchone()[0]
        if "executed successfully" in message.lower():
            print("Masking Policy applied to tag successfully")
    except Exception as e:
        print("Exception Occured: {e}")
def apply_tag_to_columns():
    try:
        print(f"""--------->Applying tag {tag_name} to columns""")
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_1_POS set tag {database}.{schema}.data_sensitivity = 'FLOAT_MASK' """)
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_2A_POS set tag {database}.{schema}.data_sensitivity = 'FLOAT_MASK' """)
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_2B_POS set tag {database}.{schema}.data_sensitivity = 'FLOAT_MASK' """)
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_2_POS set tag {database}.{schema}.data_sensitivity = 'FLOAT_MASK' """)
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_3_POS set tag {database}.{schema}.data_sensitivity = 'FLOAT_MASK' """)
        print("Tags applied to columns")
    except Exception as e:
        print("Exception Occurred:{e}")
def untag_columns():
    try:
        print(f"""--------->Unsetting tag {tag_name} from columns""")
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_1_POS unset tag {database}.{schema}.data_sensitivity """)
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_2A_POS unset tag {database}.{schema}.data_sensitivity """)
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_2B_POS unset tag {database}.{schema}.data_sensitivity """)
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_2_POS unset tag {database}.{schema}.data_sensitivity """)
        cur.execute(f"""alter view {database}.{p360_schema}.VW_PROJECT_INDICATION_FLAT modify column 
                    GOV_APPROVED_PHASE_3_POS unset tag {database}.{schema}.data_sensitivity """)
        print("Tags unsetting done")
    except Exception as e:
        print("Exception Occurred:{e}")
    
create_tag_data_sensitivity()
create_masking_policies()
apply_policies_to_tag()
apply_tag_to_columns()
# untag_columns()
Modify_masking_policies()
       
                        
                    

