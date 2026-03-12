{{ config(materialized='view') }}

with indication_data as (

    select
        clinical_ind,
        project_ind_status
    from {{ source('srv_mdm_rndmasterdata','vw_mdm_project_ind_master') }}
    where project_ind_status in ('ongoing', 'completed', 'stopped')
      and clinical_ind not like 'comm%'

),

snomed_mapping as (

    select
        meddra_llt_code,
        snomed_ct_code
    from {{ source('stg_manual_inputs','meddra_snomed_ct_mapping') }}

)

select distinct
    ind.clinical_ind        as clinical_ind,
    snomed.meddra_llt_code  as meddra_llt_code,
    snomed.snomed_ct_code   as snomed_ct_code
from indication_data ind
left join snomed_mapping snomed
    on snomed.meddra_llt_code = ind.clinical_ind