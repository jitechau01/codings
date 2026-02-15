with VW_MDM_CLINICAL_INDICATION as (

select * from {{ source('mdm', 'MDM_CLINICAL_INDICATION') }}

)
select * from VW_MDM_CLINICAL_INDICATION