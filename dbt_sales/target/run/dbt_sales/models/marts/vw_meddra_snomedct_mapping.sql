
  create or replace   view working.p360.vw_meddra_snomedct_mapping
  
  
  
  
  as (
    with VW_MEDDRA_SNOMEDCT_MAPPING as (
select 
distinct indmdm.clinical_ind as clinical_ind, 
snomedct.meddra_llt_code as meddra_llt_code, 
snomedct.snomed_ct_code as SNOMED_CT_CODE
from SRV_MDM_RNDMASTERDATA.vw_mdm_project_ind_master indmdm
left join stg_manual_inputs.meddra_snomed_ct_mapping snomedct on snomedct.meddra_llt_code = indmdm.clinical_ind
where indmdm.project_ind_status in ('Ongoing', 'Completed', 'Stopped')
and indmdm.clinical_ind not like 'COMM%'
)
select * from VW_MEDDRA_SNOMEDCT_MAPPING
  );

