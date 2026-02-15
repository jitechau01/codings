with vw_indication as (

select * from {{ source('srv', 'INDICATION') }}

)
select * from vw_indication