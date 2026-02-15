
  create or replace   view working.public.vw_mdm_project_ind_master
  
  
  
  
  as (
    with VW_MDM_PROJECT_IND_MASTER as (

select * from working.srv_mdm_rndmasterdata.MDM_PROJECT_IND_MASTER

)
select * from VW_MDM_PROJECT_IND_MASTER
  );

