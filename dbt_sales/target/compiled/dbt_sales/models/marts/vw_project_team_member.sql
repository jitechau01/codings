with vw_project_team_member
as 
(select * from (
SELECT TM.PRJ_CD as PROJECT_CODE, TM.IND_UNIQUE_CD as INDICATION_UNIQUE_CODE,TM.PTM_TEAMS as PROJECT_TEAM_MEMBER_TEAMS,TM.PTM_PRJ_ROLE AS PROJECT_TEAM_MEMBER_PROJECT_ROLE_ORIG,
TM.PTM_MEMBER_DESC as PROJECT_TEAM_MEMBER_DESC,TM.PTM_EMAIL as PROJECT_TEAM_MEMBER_EMAIL,TM.PTM_SUB_TEAMS as PROJECT_TEAM_MEMBER_SUB_TEAMS,
CASE when (TM.DEPARTMENT_CODE is null or TM.DEPARTMENT_CODE = '') and (lower(TM.PTM_PRJ_ROLE) = lower('Global Regulatory Leader')
or lower(TM.PTM_PRJ_ROLE) = lower('Global Regulatory Team Leader') or lower(TM.PTM_PRJ_ROLE) = lower('GRA Team Leader'))
then 'FA10' ELSE TM.DEPARTMENT_CODE END AS PROJECT_TEAM_MEMBER_DEPARTMENT_CODE,
CASE when (TM.FUNCTION is null or TM.FUNCTION = '') and (lower(TM.PTM_PRJ_ROLE) = lower('Global Regulatory Leader')
or lower(TM.PTM_PRJ_ROLE) = lower('Global Regulatory Team Leader') or lower(TM.PTM_PRJ_ROLE) = lower('GRA Team Leader'))
then 'GRA' ELSE TM.FUNCTION END AS PROJECT_TEAM_MEMBER_FUNCTION,
scope_desc as PROJECT_TEAM_MEMBER_SCOPE_DESC,
CASE WHEN (ptm_prj_role = 'Global Project Manager' OR ptm_prj_role = 'Global Project Head' OR ptm_prj_role = 'PM' OR ptm_prj_role = 'PH' OR ptm_prj_role = 'GPM' OR ptm_prj_role = 'GPH'  )	
THEN 'GPH/GPM'
WHEN (ptm_prj_role in ('CMC Project Manager','CMC PM','CMC Leader','CMC Project Leader'))
THEN 'Function Team Lead'
WHEN (scope_desc='Research pharma' and TM.DEPARTMENT_CODE in('CL14','CA10','CL11','CL16'))
THEN 'Function Team Lead'

--AND 
WHEN ((ptm_teams = 'GPT - Core Team' OR ptm_teams = 'Core team'))
--OR ((LEFT(DEPARTMENT_CODE,2) = 'JD' OR DEPARTMENT_CODE = 'YC15' OR DEPARTMENT_CODE = 'YC10'))
--OR DEPARTMENT_CODE = 'YC11' OR DEPARTMENT_CODE = 'YC16' OR DEPARTMENT_CODE = 'YE13' OR DEPARTMENT_CODE = 'YE10' ) AND (ptm_teams = 'GPT - Core Team' OR ptm_teams = 'Core team'))
THEN 'Function Team Lead'
--WHEN ((ptm_teams = 'GPT - Extended Team' OR ptm_teams = 'Extended team')) 
--(LEFT(DEPARTMENT_CODE,2) = 'JD' OR DEPARTMENT_CODE = 'YC15' OR DEPARTMENT_CODE = 'YC10'
--OR DEPARTMENT_CODE = 'YC11' OR DEPARTMENT_CODE = 'YC16' OR DEPARTMENT_CODE = 'YE13' OR DEPARTMENT_CODE = 'YE10' OR ptm_prj_role = 'CMC OPCM')
--THEN 'Function Reader' 
--WHEN (ptm_teams = 'GPT - Core Team') AND (DEPARTMENT_CODE = 'CL10' OR DEPARTMENT_CODE = 'CL18' OR DEPARTMENT_CODE = 'CL20')
--THEN 'Function Team Lead'
--WHEN (DEPARTMENT_CODE = 'CL10' OR DEPARTMENT_CODE = 'CL18' OR DEPARTMENT_CODE = 'CL20')
--THEN 'Function Reader'
--WHEN (ptm_teams = 'GPT - Core Team' OR ptm_teams = 'Core team' ) AND (DEPARTMENT_CODE = 'FA10')
--THEN 'Function Team Lead'
--WHEN (DEPARTMENT_CODE = 'FA10')
--THEN 'Function Reader'
--WHEN (ptm_teams = 'GPT - Core Team') AND (DEPARTMENT_CODE = 'CL12')
--THEN 'Function Team Lead'
--WHEN (DEPARTMENT_CODE = 'CL12')
--THEN 'Function Reader'
--WHEN (ptm_teams = 'GPT - Core Team' OR ptm_teams = 'Core team') AND (LEFT(DEPARTMENT_CODE,2) = 'DB' OR DEPARTMENT_CODE ='YA10' 
--OR DEPARTMENT_CODE ='YJ14' OR DEPARTMENT_CODE ='YC12' OR DEPARTMENT_CODE ='YA20' )
--THEN 'Function Team Lead'
--WHEN (LEFT(DEPARTMENT_CODE,2) = 'DB' OR DEPARTMENT_CODE ='YA10' 
--OR DEPARTMENT_CODE ='YJ14' OR DEPARTMENT_CODE ='YC12' OR DEPARTMENT_CODE ='YA20'
--OR PTM_SUB_TEAMS='CSO Subteam'
--)
--THEN 'Function Reader'
/*WHEN (ptm_teams = 'Core team') AND ( DEPARTMENT_CODE ='YD13' OR DEPARTMENT_CODE ='YJ10' OR DEPARTMENT_CODE ='YJ15' OR DEPARTMENT_CODE ='YD12' OR DEPARTMENT_CODE ='YD14'  )
THEN 'Function Team Lead'
WHEN  ( DEPARTMENT_CODE ='YD13' OR DEPARTMENT_CODE ='YJ10' OR DEPARTMENT_CODE ='YJ15' OR DEPARTMENT_CODE ='YD12'  OR DEPARTMENT_CODE ='YD14')
THEN 'Function Reader'
WHEN (ptm_teams = 'Core team') AND ( DEPARTMENT_CODE ='YE18')
THEN 'Function Team Lead'
WHEN (DEPARTMENT_CODE ='YE18')
THEN 'Function Reader'
WHEN (PRJ_CATEGORIE || ' ' || PRJ_VACCIN_PHARMA = 'Research pharma') AND ( DEPARTMENT_CODE ='CL14')
THEN 'Function Team Lead'
WHEN (DEPARTMENT_CODE ='CL14')
THEN 'Function Reader'
WHEN (PRJ_CATEGORIE || ' ' || PRJ_VACCIN_PHARMA = 'Research pharma') AND ( DEPARTMENT_CODE ='CA10')
THEN 'Function Team Lead'
WHEN (DEPARTMENT_CODE ='CA10')
THEN 'Function Reader'
WHEN (PRJ_CATEGORIE || ' ' || PRJ_VACCIN_PHARMA = 'Research pharma') AND ( DEPARTMENT_CODE ='CL11')
THEN 'Function Team Lead'
WHEN (DEPARTMENT_CODE ='CL11')
THEN 'Function Reader'
WHEN (PRJ_CATEGORIE || ' ' || PRJ_VACCIN_PHARMA = 'Research pharma') AND ( DEPARTMENT_CODE ='CL16')
THEN 'Function Team Lead'
WHEN (DEPARTMENT_CODE ='CL16')
THEN 'Function Reader'
WHEN (ptm_teams = 'GPT - Core Team') AND ( left(DEPARTMENT_CODE,2) ='BK')
THEN 'Function Team Lead'
WHEN (left(DEPARTMENT_CODE,2) ='BK' OR PTM_SUB_TEAMS='Translational subteam' )
THEN 'Function Reader'
 
WHEN (ptm_teams = 'GPT - Core Team' OR ptm_teams = 'Core team')	
THEN 'Other'
*/
ELSE 'Other'
END AS PROJECT_TEAM_MEMBER_PROJECT_ROLE	
FROM
(
select distinct prj_cd 
    ,null as ind_unique_cd  
    ,tmb.ptm_teams
    ,tmb.ptm_prj_role
    ,tmb.ptm_member_desc
    ,tmb.ptm_email
    ,tmb.ptm_sub_teams
	,case when  UPPER(prj_tpr_category) = UPPER('R') then  'Research'
     when UPPER(prj_tpr_category) = UPPER('D') then  'Development'
     when UPPER(tpr.tpr_desc) =  UPPER('Others')  then 'Other' else tpr.tpr_desc end||' '|| case when prj_vaccin_flag= TRUE then 'vaccin' 
	else 'pharma'end as scope_desc
	,substr(res.RES_SERVICE_FOU_FK,1,4) as Department_code,
case when (substr(res.RES_SERVICE_FOU_FK,1,4) in ('YC15', 'YC10' , 'YC11' ,'YC16' , 'YE13', 'YE10') or substr(res.RES_SERVICE_FOU_FK,1,2) = 'JD' or tmb.ptm_prj_role in ('CMC Project Manager','CMC PM','CMC Leader','CMC Project Leader')) then 'CMC'
    when substr(res.RES_SERVICE_FOU_FK,1,4) in ('CL10','CL18','CL20') then 'LMR'
    when substr(res.RES_SERVICE_FOU_FK,1,4) = 'FA10' then 'GRA'
    when substr(res.RES_SERVICE_FOU_FK,1,4) = 'CL12' then 'IDD'
    when (substr(res.RES_SERVICE_FOU_FK,1,4) in ('YA10', 'YA20' , 'YC12' ,'YJ14','YJ11') or substr(res.RES_SERVICE_FOU_FK,1,2) = 'DB') then 'CSO'
    when substr(res.RES_SERVICE_FOU_FK,1,4) in ('YD13','YJ10','YJ15' ,'YD12' ,'YD14','YJ13','YD11')  then 'Res Vx'
    when substr(res.RES_SERVICE_FOU_FK,1,4) = 'YE18' then 'mRNA CoE'
    when substr(res.RES_SERVICE_FOU_FK,1,4) = 'CL14' then 'PCS'
    when substr(res.RES_SERVICE_FOU_FK,1,4) = 'CA10' then 'PMCB'
    when substr(res.RES_SERVICE_FOU_FK,1,4) = 'CL11' then 'DMPK'
    when substr(res.RES_SERVICE_FOU_FK,1,4) = 'CL16' then 'TIM'
    when substr(res.RES_SERVICE_FOU_FK,1,2)= 'BK' or 
	substr(res.RES_SERVICE_FOU_FK,1,4) in ('LA10','LA11','LA12','LA13','LA14','LA15','LA16','LA17')
	then 'TMU'
    else NULL end as Function,
    case when prj_pharma_flag = true and prj_vaccin_flag = false then 'pharma' else 'vaccin' end as prj_vaccin_pharma,
    case when  UPPER(prj_tpr_category) = UPPER('R') then  'Research'
     when UPPER(prj_tpr_category) = UPPER('D') then  'Development'
     when UPPER(tpr_desc) =  UPPER('Others')  then 'Other' else tpr.tpr_desc end AS prj_categorie
    from SRV_RND_DF.mvw_wbs_hierarchy wbs
    join SRV_RND_DF.vw_ref_baseline bas
      on wbs.time_id = bas.time_id
    left join SRV_RND_DF.vw_project prj
      on prj.prj_wbs_id = wbs.project_id
      and prj.time_id = wbs.time_id 
      and prj_status_detailed in ('Ongoing','Completed inactive','Completed active','Stopped inactive','Stopped active')
    left join SRV_RND_DF.vw_indication ind
      on ind.ind_wbs_id = wbs.indication_id
      and ind.time_id = wbs.time_id 
	left join SRV_RND_DF.vw_team_member tmb
      on tmb.wbs_id = wbs.wbs_id
     and tmb.time_id = wbs.time_id
     left join STG_MANUAL_INPUTS.project_type tpr
    on tpr.tpr_id = prj.prj_tpr_fk
	left join srv_rnd_df.vw_resource res
      ON UPPER(res.res_network_id)=UPPER(tmb.ptm_sanofi_id)
      and res.time_id=wbs.time_id
      and res_inactive_flag=FALSE
      and res.res_network_id is not null
    where bas.bas_desc in ('Live') -- Live Data
    and ptm_member_desc is not null
    and ptm_teams is not null
	and UPPER(prj.CREATED_BY)='RDPM'  --Filtering FIRST data
    and  ( prj_cd not like ('OC%') and  prj_cd not like ('RC%') and prj_cd not like ('DC%') and prj_cd not like ('POLY_%') and prj_cd not like ('RC%') )
) TM
) where PROJECT_TEAM_MEMBER_PROJECT_ROLE!='Other'
)
select * from vw_project_team_member