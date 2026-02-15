
  create or replace   view working.public.vw_ref_baseline
  
  
  
  
  as (
    with VW_REF_BASELINE as (

select * from working.srv_rnd_df.REF_BASELINE

)
select * from VW_REF_BASELINE
  );

