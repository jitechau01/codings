
  create or replace   view working.public.vw_project
  
  
  
  
  as (
    with VW_PROJECT as (

select * from working.srv_rnd_df.PROJECT

)
select * from VW_PROJECT
  );

