
  create or replace   view working.public.vw_indication
  
  
  
  
  as (
    with vw_indication as (

select * from working.srv_rnd_df.INDICATION

)
select * from vw_indication
  );

