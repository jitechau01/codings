{{ config(materialized='view') }}

with project_tcp as (

    select *
    from {{ source('landing','project_tcp') }}

)

select *
from project_tcp