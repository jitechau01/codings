{{ config(materialized='view') }}

with project_team_member as (

    select *
    from {{ source('landing','project_team_member')}}

)

select *
from project_team_member