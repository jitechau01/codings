import os
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_data_engineer import _conn

cur=_conn()
database='rndcontrolling'
srv_layer_schema='srv_rnd_df'
dp_rdportfolio360_schema='dp_rdportfolio360'
crdh_dea_iport_reporting_schema='crdh_dea_iport_reporting'
srv_mdm_rndmasterdata_schema='srv_mdm_rndmasterdata'
stg_manual_inputs_schema='stg_manual_inputs'

def create_srv_rnd_df_views():  
    cur.execute(f"""use schema {database}.srv_rnd_df""")
    print("\n-----------view Creation Starts-------------------")
    try: 
        result=cur.execute("""create view if not exists MVW_WBS_HIERARCHY as select * from LANDING.WBS_HIERARCHY """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view MVW_WBS_HIERARCHY successfully created")
                elif "already exists" in message:
                    print("MVW_WBS_HIERARCHY view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view MVW_WBS_HIERARCHY: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists VW_INDICATION as select * from landing.indication """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_INDICATION successfully created")
                elif "already exists" in message:
                    print("VW_INDICATION view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_INDICATION: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists VW_PHASE as select * from landing.phase """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PHASE successfully created")
                elif "already exists" in message:
                    print("VW_PHASE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PHASE: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists VW_PROJECT as select * from landing.project """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT: {e}")
        

    try: 
        result=cur.execute("""create view if not exists VW_REF_BASELINE as select * from landing.ref_baseline """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_REF_BASELINE successfully created")
                elif "already exists" in message:
                    print("VW_REF_BASELINE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_REF_BASELINE: {e}")
                
    try: 
        result=cur.execute("""create view if not exists VW_TASK as select * from landing.task """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_TASK successfully created")
                elif "already exists" in message:
                    print("VW_TASK view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_TASK: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists VW_TEAM_MEMBER as select * from landing.team_member """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_TEAM_MEMBER successfully created")
                elif "already exists" in message:
                    print("VW_TEAM_MEMBER view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_TEAM_MEMBER: {e}")       
def create_srv_mdm_rndmasterdata_views(): 
    cur.execute(f"""use schema {database}.srv_mdm_rndmasterdata""")
    print("\n-----------view Creation Starts for schema srv_mdm_rndmasterdata-------------------")
    try: 
        result=cur.execute("""create view if not exists VW_MDM_CLINICAL_INDICATION as select * from landing.mdm_clinical_indication """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MDM_CLINICAL_INDICATION successfully created")
                elif "already exists" in message:
                    print("VW_MDM_CLINICAL_INDICATION view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MDM_CLINICAL_INDICATION: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists VW_MDM_FINANCIAL_ORGANIZATION_UNIT as select * from landing.mdm_financial_organization_unit """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MDM_FINANCIAL_ORGANIZATION_UNIT successfully created")
                elif "already exists" in message:
                    print("VW_MDM_FINANCIAL_ORGANIZATION_UNIT view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MDM_FINANCIAL_ORGANIZATION_UNIT: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists VW_MDM_PROJECT_IND_MASTER as select * from landing.mdm_project_ind_master """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MDM_PROJECT_IND_MASTER successfully created")
                elif "already exists" in message:
                    print("VW_MDM_PROJECT_IND_MASTER view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MDM_PROJECT_IND_MASTER: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists VW_MDM_PROJECT_MASTER as select * from landing.mdm_project_master """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MDM_PROJECT_MASTER successfully created")
                elif "already exists" in message:
                    print("VW_MDM_PROJECT_MASTER view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MDM_PROJECT_MASTER: {e}")          
def create_stg_manual_inputs_views():  
    cur.execute(f"""use schema {database}.stg_manual_inputs""")
    print("\n-----------view Creation Starts for schema stg_manual_inputs-------------------")
    try: 
        result=cur.execute("""create view if not exists ICD10_MEDDRA_MAPPING as select * from landing.ICD10_MEDDRA_MAPPING """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view ICD10_MEDDRA_MAPPING successfully created")
                elif "already exists" in message:
                    print("ICD10_MEDDRA_MAPPING view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view ICD10_MEDDRA_MAPPING: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists MEDDRA_SNOMED_CT_MAPPING as select * from landing.MEDDRA_SNOMED_CT_MAPPING """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view MEDDRA_SNOMED_CT_MAPPING successfully created")
                elif "already exists" in message:
                    print("MEDDRA_SNOMED_CT_MAPPING view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view MEDDRA_SNOMED_CT_MAPPING: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists PROJECT_TYPE as select * from landing.PROJECT_TYPE """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view PROJECT_TYPE successfully created")
                elif "already exists" in message:
                    print("PROJECT_TYPE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view PROJECT_TYPE: {e}")             
def create_crdh_dea_iport_reporting_views():
    cur.execute(f"""use schema {database}.crdh_dea_iport_reporting""")
    print("\n-----------view Creation Starts for schema crdh_dea_iport_reporting-------------------")
    try: 
        result=cur.execute("""create view if not exists PRTFL_TCP_PROFILE as select * from landing.PRTFL_TCP_PROFILE """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view PRTFL_TCP_PROFILE successfully created")
                elif "already exists" in message:
                    print("PRTFL_TCP_PROFILE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view PRTFL_TCP_PROFILE: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists PRTFL_TPP_PROFILE as select * from landing.prtfl_tpp_profile """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view PRTFL_TPP_PROFILE successfully created")
                elif "already exists" in message:
                    print("PRTFL_TPP_PROFILE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view PRTFL_TPP_PROFILE: {e}")
        
        
    try: 
        result=cur.execute("""create view if not exists PRTFL_TVP_PROFILE as select * from landing.PRTFL_TVP_PROFILE """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view PRTFL_TVP_PROFILE successfully created")
                elif "already exists" in message:
                    print("PRTFL_TVP_PROFILE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view PRTFL_TVP_PROFILE: {e}")
def create_dp_rdportfolio360_views():
    cur.execute(f"""use schema {database}.{ dp_rdportfolio360_schema}""")
    print(f"\n-----------view Creation Starts for schema {dp_rdportfolio360_schema}-------------------")
    try: 
        result=cur.execute("""create view if not exists  VW_MEDDRA_ICD10_MAPPING(
	SANOFI_MEDDRA_INDICATION_CODE,
	ICD10_CODE_2019_INTL_CORE_VER,
	MEDDRA_PT_CODE,
	MEDDRA_LLT_CODE
) COMMENT='Maps MEDDRA codes to ICD10 codes for indications used in Sanofi Project Indications. This is filtered to Indications with a status of Ongoing, Completed, or Stopped and excludes the COMMON placeholder indication. The basis of this is the indication data in the R&D MDM and the mapping data from MedDRA'
 as
(select distinct indmdm.clinical_ind, icd10.icd10_code_2019_intl_core_ver, icd10.meddra_pt_code, icd10.mapped_meddra_llt_code
from SRV_MDM_RNDMASTERDATA.vw_mdm_project_ind_master indmdm
left join stg_manual_inputs.icd10_meddra_mapping icd10 on (icd10.meddra_pt_code = indmdm.clinical_ind or icd10.mapped_meddra_llt_code = indmdm.clinical_ind)
where indmdm.project_ind_status in ('Ongoing', 'Completed', 'Stopped')
and indmdm.clinical_ind not like 'COMM%')
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MEDDRA_ICD10_MAPPING successfully created")
                elif "already exists" in message:
                    print("VW_MEDDRA_ICD10_MAPPING view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MEDDRA_ICD10_MAPPING: {e}") 
        
    try: 
        result=cur.execute("""create view if not exists  VW_MEDDRA_SNOMEDCT_MAPPING(
	CLINICAL_IND,
	MEDDRA_LLT_CODE,
	SNOMED_CT_CODE
) COMMENT='Maps MEDDRA codes to SNOMED CT codes for indications used in Sanofi Project Indications. This is filtered to Indications with a status of Ongoing, Completed, or Stopped and excludes the COMMON placeholder indication. The basis of this is the indication data in the R&D MDM and the SNOMED CT mapping data from MedDRA'
 as
(
select distinct indmdm.clinical_ind as clinical_ind, snomedct.meddra_llt_code as meddra_llt_code, snomedct.snomed_ct_code as SNOMED_CT_CODE
from SRV_MDM_RNDMASTERDATA.vw_mdm_project_ind_master indmdm
left join stg_manual_inputs.meddra_snomed_ct_mapping snomedct on snomedct.meddra_llt_code = indmdm.clinical_ind
where indmdm.project_ind_status in ('Ongoing', 'Completed', 'Stopped')
and indmdm.clinical_ind not like 'COMM%')
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MEDDRA_SNOMEDCT_MAPPING successfully created")
                elif "already exists" in message:
                    print("VW_MEDDRA_SNOMEDCT_MAPPING view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MEDDRA_SNOMEDCT_MAPPING: {e}")
             
    try: 
        result=cur.execute("""create view if not exists VW_PROJECT_INDICATION_TPP as select * from landing.PROJECT_INDICATION_TPP """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_INDICATION_TPP successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_INDICATION_TPP view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_INDICATION_TPP: {e}")
        
    try: 
        result=cur.execute("""create view if not exists VW_PROJECT_TCP as select * from landing.PROJECT_TCP """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_TCP successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_TCP view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_TCP: {e}")
        
    try: 
        result=cur.execute("""create view if not exists VW_PROJECT_TVP as select * from landing.PROJECT_TVP """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_TVP successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_TVP view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_TVP: {e}")
        
    try: 
        result=cur.execute("""create view if not exists VW_PROJECT_TEAM_MEMBER as select * from landing.PROJECT_TEAM_MEMBER """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_TEAM_MEMBER successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_TEAM_MEMBER view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_TEAM_MEMBER: {e}")
        
    try: 
        result=cur.execute("""create view if not exists VW_PROJECT_INDICATION_FLAT as select * from landing.PROJECT_INDICATION_FLAT """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_INDICATION_FLAT successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_INDICATION_FLAT view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_INDICATION_FLAT: {e}")
    
create_srv_rnd_df_views()
create_srv_mdm_rndmasterdata_views()
create_stg_manual_inputs_views()
create_crdh_dea_iport_reporting_views()
create_dp_rdportfolio360_views()