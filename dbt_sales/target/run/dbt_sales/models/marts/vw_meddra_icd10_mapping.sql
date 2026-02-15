
  create or replace   view working.p360.vw_meddra_icd10_mapping
  
  
  
  
  as (
    with vw_meddra_icd10_mapping as (
    select 
    distinct indmdm.clinical_ind, 
    icd10.icd10_code_2019_intl_core_ver, 
    icd10.meddra_pt_code, 
    icd10.mapped_meddra_llt_code
from SRV_MDM_RNDMASTERDATA.vw_mdm_project_ind_master indmdm
left join stg_manual_inputs.icd10_meddra_mapping icd10 
on (icd10.meddra_pt_code = indmdm.clinical_ind or icd10.mapped_meddra_llt_code = indmdm.clinical_ind)
where indmdm.project_ind_status in ('Ongoing', 'Completed', 'Stopped')
and indmdm.clinical_ind not like 'COMM%'
)
select * from vw_meddra_icd10_mapping
  );

