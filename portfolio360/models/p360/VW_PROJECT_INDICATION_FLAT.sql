{{ config(materialized='view') }}

with project_indication_flat as (

    select *
    from {{ source('landing','project_indication_flat') }}

)

select *
from project_indication_flat