with VW_MDM_PROJECT_IND_MASTER as (

select * from {{ source('mdm', 'MDM_PROJECT_IND_MASTER') }}

)
select * from VW_MDM_PROJECT_IND_MASTER