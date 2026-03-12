{{ config(materialized='view') }}

with project_indication_tpp as (

    select *
    from {{ source('landing','project_indication_tpp') }}

)

select *
from project_indication_tpp