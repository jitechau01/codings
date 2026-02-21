from snowflake_pythons.__connections.__con_lead import _conn_lead

cur=_conn_lead()
database='rndcontrolling'
consumer_role='data_consumer'
p360_schema='DP_RDPORTFOLIO360'

def create_masking_policies():
    cur.execute("""create or replace masking policy rndcontrolling.datasecurity.float_policy as (val float) returns float ->
                    case
                        WHEN EXISTS (
                        with cd as
                                (select l.database_name,l.schema_name,l.consumer_name,r.user_name,l.access_type 
                                from rndcontrolling.datasecurity.consumers_access_control l,rndcontrolling.datasecurity.consumer_user_details r 
                                where l.consumer_name=r.consumer_name),
                                cu as (select upper(current_user)  as current_user)
                                select distinct cd.consumer_name from cd,cu
                                where upper(cd.user_name)=cu.current_user
                                and upper(cd.database_name)=upper(current_database())
                                and upper(cd.schema_name)=upper(current_schema())
                                and upper(cd.access_type)='MASKED'
                        )
                        THEN .00000001
                        ELSE NVL(VAL,0)
                    END)"""
    )
def create_tag_data_sensitivity():
    cur.execute("""CREATE tag if not exists rndcontrolling.datasecurity.data_sensitivity ALLOWED_VALUES 'NUMBER_MASK','STRING_MASK',
                'FLOAT_MASK,DATE_MASK,BOOLEAN_MASK""")    
def apply_policies_to_tag():
    cur.execute("""ALTER TAG rndcontrolling.datasecurity.data_sensitivity SET MASKING POLICY 
                working.datasecurity.float_policy""")   
def apply_tag_to_columns():
    cur.execute("""alter view rndcontrolling.dp_rdportfolio360.VW_PROJECT_INDICATION_FLAT modify column 
                GOV_APPROVED_PHASE_1_POS set tag working.datasecurity.data_sensitivity = 'NUMBER_MASK' """)
    cur.execute("""alter view rndcontrolling.dp_rdportfolio360.VW_PROJECT_INDICATION_FLAT modify column 
                GOV_APPROVED_PHASE_2A_POS set tag working.datasecurity.data_sensitivity = 'NUMBER_MASK' """)
    cur.execute("""alter view rndcontrolling.dp_rdportfolio360.VW_PROJECT_INDICATION_FLAT modify column 
                GOV_APPROVED_PHASE_2B_POS set tag working.datasecurity.data_sensitivity = 'NUMBER_MASK' """)
    cur.execute("""alter view rndcontrolling.dp_rdportfolio360.VW_PROJECT_INDICATION_FLAT modify column 
                GOV_APPROVED_PHASE_2_POS set tag working.datasecurity.data_sensitivity = 'NUMBER_MASK' """)
    cur.execute("""alter view rndcontrolling.dp_rdportfolio360.VW_PROJECT_INDICATION_FLAT modify column 
                GOV_APPROVED_PHASE_3_POS set tag working.datasecurity.data_sensitivity = 'NUMBER_MASK' """)

create_masking_policies()
create_tag_data_sensitivity()
apply_policies_to_tag()
apply_tag_to_columns()
       
                        
                    

