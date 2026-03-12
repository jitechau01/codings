{{ config(materialized='view') }}

with project_tvp as (

    select *
    from {{ source('landing','project_tvp' )}}

)

select *
from project_tvp