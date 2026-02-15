
  create or replace   view working.public.vw_mdm_financial_organization_unit
  
  
  
  
  as (
    with VW_MDM_FINANCIAL_ORGANIZATION_UNIT as (

select * from working.srv_mdm_rndmasterdata.MDM_FINANCIAL_ORGANIZATION_UNIT

)
select * from VW_MDM_FINANCIAL_ORGANIZATION_UNIT
  );

