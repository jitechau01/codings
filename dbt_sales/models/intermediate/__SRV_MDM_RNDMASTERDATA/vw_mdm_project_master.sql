with VW_MDM_PROJECT_MASTER as (

select * from {{ source('mdm', 'MDM_PROJECT_MASTER') }}

)
select * from VW_MDM_PROJECT_MASTER