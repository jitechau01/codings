
  create or replace   view working.p360.vw_project_indication_milestone_dates
  
  
  
  
  as (
    WITH base_data AS (
    SELECT 
        prjmdm.project_code_cd AS PROJECT_CODE, 
        wbs.ind_functional_id AS INDICATION_UNIQUE_CODE, 
        tsk.tsk_activity_type AS MILESTONE_NAME, 
        tsk.tsk_planned_finish_dt AS MILESTONE_PLANNED_FINISH_DT, 
        REGEXP_SUBSTR(tsk.TSK_COMMENT, '(US|EU|JP|CN)') AS MILESTONE_COUNTRY_CODE, 
        tsk.tsk_comment AS MILESTONE_COMMENT
    FROM srv_rnd_df.vw_task tsk
    INNER JOIN srv_rnd_df.mvw_wbs_hierarchy wbs 
        ON wbs.wbs_id = tsk.tsk_wbs_id AND wbs.time_id = tsk.time_id
    INNER JOIN SRV_MDM_RNDMASTERDATA.vw_mdm_project_master prjmdm 
        ON prjmdm.project_code_cd = wbs.prj_functional_id
    INNER JOIN srv_rnd_df.vw_ref_baseline bas 
        ON bas.time_id = wbs.time_id AND bas.bas_desc = 'Live'
    WHERE tsk.is_last = TRUE
        AND tsk.tsk_activity_type IN ('Target Selection - M0', 'Lead Selection - M1',  'Pre Candidate Selection', 'Start Development - M2', 'Proof of Commercial Concept','Start Ph01',  'Start Ph02', 'Start Ph2A','Start Ph2B','Start Ph03','First Submission', 'First Approval', 'Submission', 'Approval')
        AND prjmdm.project_category IN ('R','D')
        AND prjmdm.project_organization_type IN ('RESEARCH', 'DEVELOPMENT', 'VACCINE')
        AND prjmdm.project_status IN ('Ongoing', 'Completed')
        AND prjmdm.project_phase IN ('M0-M1','M1-M2','M0-M2','Preclinical','Phase 1','Phase 2','Phase 2A','Phase 2B','Phase 3','Regulatory submission','LCM')
),

-- Get the LAST milestone (most recent completed: date <= today)
last_milestone AS (
    SELECT 
        PROJECT_CODE,
        INDICATION_UNIQUE_CODE,
        MILESTONE_NAME AS LAST_MILESTONE,
        MILESTONE_PLANNED_FINISH_DT,
    FROM (
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY PROJECT_CODE, INDICATION_UNIQUE_CODE 
                               ORDER BY MILESTONE_PLANNED_FINISH_DT DESC) AS rn
        FROM base_data
        WHERE MILESTONE_PLANNED_FINISH_DT <= CURRENT_DATE()
    )
    WHERE rn = 1
),

-- Get the NEXT milestone (earliest upcoming: date > today)
next_milestone AS (
    SELECT 
        PROJECT_CODE,
        INDICATION_UNIQUE_CODE,
        MILESTONE_NAME AS NEXT_MILESTONE,
        MILESTONE_PLANNED_FINISH_DT,
        MILESTONE_COUNTRY_CODE,
        MILESTONE_COMMENT
    FROM (
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY PROJECT_CODE, INDICATION_UNIQUE_CODE 
                               ORDER BY MILESTONE_PLANNED_FINISH_DT ASC) AS rn
        FROM base_data
        WHERE MILESTONE_PLANNED_FINISH_DT > CURRENT_DATE()
    )
    WHERE rn = 1
)

-- Final output: Join last and next milestones into single row
SELECT 
    COALESCE(n.PROJECT_CODE, l.PROJECT_CODE) AS PROJECT_CODE,
    COALESCE(n.INDICATION_UNIQUE_CODE, l.INDICATION_UNIQUE_CODE) AS INDICATION_UNIQUE_CODE,
    --n.MILESTONE_PLANNED_FINISH_DT,
    --n.MILESTONE_COUNTRY_CODE as MILESTONE_COUNTRY_CODE,
    --n.MILESTONE_COMMENT,
    l.LAST_MILESTONE,
    l.MILESTONE_PLANNED_FINISH_DT as LAST_MILESTONE_FINISH_DT,
    n.NEXT_MILESTONE,
    n.MILESTONE_PLANNED_FINISH_DT as NEXT_MILESTONE_PLANNED_FINISH_DT
FROM next_milestone n
FULL OUTER JOIN last_milestone l 
    ON n.PROJECT_CODE = l.PROJECT_CODE 
    AND n.INDICATION_UNIQUE_CODE = l.INDICATION_UNIQUE_CODE
ORDER BY PROJECT_CODE, INDICATION_UNIQUE_CODE
  );

