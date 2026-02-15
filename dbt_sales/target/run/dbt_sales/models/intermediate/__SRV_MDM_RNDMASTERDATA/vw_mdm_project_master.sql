
  create or replace   view working.public.vw_mdm_project_master
  
  
  
  
  as (
    with VW_MDM_PROJECT_MASTER as (

select * from working.srv_mdm_rndmasterdata.MDM_PROJECT_MASTER

)
select * from VW_MDM_PROJECT_MASTER
  );

