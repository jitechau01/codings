with VW_PROJECT as (

select * from {{ source('srv', 'PROJECT') }}

)
select * from VW_PROJECT