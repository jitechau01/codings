with VW_REF_BASELINE as (

select * from {{ source('srv', 'REF_BASELINE') }}

)
select * from VW_REF_BASELINE