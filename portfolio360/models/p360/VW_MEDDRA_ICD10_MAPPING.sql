{{ config(materialized='view') }}

with source_indication as (

    select
        clinical_ind,
        project_ind_status
    from {{ source('srv_mdm_rndmasterdata', 'vw_mdm_project_ind_master') }}
    where project_ind_status in ('ongoing','completed','stopped')
      and clinical_ind not like 'comm%'

),

icd10_mapping as (

    select
        icd10_code_2019_intl_core_ver,
        meddra_pt_code,
        mapped_meddra_llt_code
    from {{ source('stg_manual_inputs', 'icd10_meddra_mapping') }}

)

select distinct
    ind.clinical_ind                as sanofi_meddra_indication_code,
    icd10.icd10_code_2019_intl_core_ver,
    icd10.meddra_pt_code            as meddra_pt_code,
    icd10.mapped_meddra_llt_code    as meddra_llt_code
from source_indication ind
left join icd10_mapping icd10
    on icd10.meddra_pt_code = ind.clinical_ind
    or icd10.mapped_meddra_llt_code = ind.clinical_ind