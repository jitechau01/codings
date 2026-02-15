
  create or replace   view working.public.vw_mdm_clinical_indication
  
  
  
  
  as (
    with VW_MDM_CLINICAL_INDICATION as (

select * from working.srv_mdm_rndmasterdata.MDM_CLINICAL_INDICATION

)
select * from VW_MDM_CLINICAL_INDICATION
  );

