
  create or replace   view working.public.vw_project_indication_flat
  
  
  
  
  as (
    WITH fou                                                                            AS (
    SELECT
        rdm_code_cd,
        CASE
            WHEN fou.EN_NM LIKE 'Oncology%' THEN 'Oncology'
            WHEN fou.EN_NM LIKE 'Immunology%' THEN 'Immuno-inflammation'
            WHEN fou.EN_NM LIKE 'Rare &amp; Neurologic Disease R - Rare'  THEN 'Rare Diseases'
            WHEN fou.EN_NM LIKE 'Rare &amp; Neurologic Disease R - Neuro' THEN 'Neurology'
            WHEN fou.EN_NM LIKE 'DCV%' THEN 'DCVM'
            WHEN fou.EN_NM LIKE 'Diabetes%' THEN 'DCVM'
            WHEN fou.EN_NM LIKE 'Transplant%' THEN 'Transplant'
            WHEN fou.EN_NM LIKE 'Genomic Medicine Unit%' THEN 'Rare Diseases'
            WHEN fou.EN_NM LIKE 'Rare Blood Disorders%' THEN 'Rare Diseases'
            WHEN fou.EN_NM LIKE '%Vaccine%' THEN 'Vaccines'
            WHEN fou.EN_NM LIKE 'Neurology%' THEN 'Neurology'
            WHEN fou.EN_NM LIKE 'Ophthalmology%' THEN 'Ophthalmology'
            ELSE fou.EN_NM
        END                                                                         AS EN_NM
    FROM SRV_MDM_RNDMASTERDATA.vw_mdm_financial_organization_unit fou
),

prjmdm                                                                              AS (
    SELECT
        prjmdm.project_code_cd,
        CASE
            WHEN prjmdm.project_category = 'D' THEN 'Development'
            WHEN prjmdm.project_category = 'R' THEN 'Research'
            ELSE prjmdm.project_category
        END                                                                         AS PROJECT_CATEGORY,
        CASE
            WHEN prjmdm.project_organization_type = 'VACCINE' THEN 'VACCINE'
            WHEN prjmdm.project_organization_type IN ('DEVELOPMENT','RESEARCH') THEN 'PHARMA'
            ELSE prjmdm.project_organization_type
        END                                                                         AS PROJECT_ORGANIZATION,
        prjmdm.project_name_nm,
        prjmdm.project_description_desc,
        prj.prj_status,
        prj.prj_phase,
        prjmdm.project_organization_type,
        prj.prj_responsability_fou_fk,
        prj.prj_brand_nm,
        prj.prj_inn,
        prjmdm.mechanism_of_action,
        prj.prj_moa_short_nm,
        prjmdm.active_substance_type,
        prjmdm.active_substance_sub_type,
        prjmdm.origin_of_active_substance,
        prj.prj_priority,
        prj.prj_innovation_status,
        prj.PRJ_DISCO_DEV_LINKED_CODES,
        prj.prj_franchise,
        prj.time_id,
        prj.PRJ_PHARMACOLOGICAL_EFFECT
    FROM SRV_MDM_RNDMASTERDATA.vw_mdm_project_master prjmdm
    JOIN (
        SELECT DISTINCT
            prj_cd, prj_phase, prj_priority, prj_responsability_fou_fk, prj_responsability_desc,
            prj_innovation_status, prj_status, prj_inn, prj_brand_nm, prj_moa_short_nm,
            PRJ_DISCO_DEV_LINKED_CODES, prj_franchise, prj.time_id,PRJ_PHARMACOLOGICAL_EFFECT
        FROM srv_rnd_df.vw_project prj
        JOIN srv_rnd_df.vw_ref_baseline bas
            ON prj.time_id = bas.time_id
        --WHERE bas.bas_desc = 'Live'
    ) prj
        ON prjmdm.project_code_cd = prj.prj_cd
    WHERE prjmdm.project_category IN ('R','D')
        AND prjmdm.project_organization_type IN ('RESEARCH','DEVELOPMENT','VACCINE')
        AND prj.prj_status IN ('Ongoing','Completed')
        AND prj.prj_phase IN ('M0-M1','M1-M2','M0-M2','Preclinical','Phase 1','Phase 2','Phase 2A','Phase 2B','Phase 3','Regulatory submission','LCM', 'Post-Launch')
),

indmdm                                                                              AS (
    SELECT
        indmdm.project_ind_code_cd,
        REGEXP_SUBSTR(indmdm.project_ind_code_cd, '^(.*?)_IND', 1, 1, 'e', 1)       AS indmdm_project_code,
        indmdm.project_ind_description_desc,
        indmdm.project_ind_name_nm,
        indmdm.clinical_ind,
        indmdm.project_ind_status,
        indmdm.project_ind_phase,
        ind.ind_fou_fk,
        ind.ind_unique_cd,
        ind.ind_lead_flag,
        ind.ind_pots,
        ind.ind_v_portfolio_strategic_grouping
    FROM SRV_MDM_RNDMASTERDATA.vw_mdm_project_ind_master indmdm
    LEFT JOIN (
        SELECT DISTINCT
            ind_unique_cd,
            ind_lead_flag,
            ind_pots,
            ind_v_portfolio_strategic_grouping,
            ind_fou_fk
        FROM srv_rnd_df.vw_indication ind
        JOIN srv_rnd_df.vw_ref_baseline bas
            ON ind.time_id = bas.time_id
        WHERE bas.bas_desc = 'Live'
    ) ind
        ON indmdm.project_ind_code_cd = ind.ind_unique_cd
    WHERE indmdm.project_ind_status IN ('Ongoing', 'Completed', 'Stopped', 'On Hold')
        AND SUBSTRING(indmdm.project_ind_code_cd, -2) NOT LIKE '5%'
),

cindmdm                                                                             AS (
    SELECT rdm_code_cd, meddra_term
    FROM SRV_MDM_RNDMASTERDATA.vw_mdm_clinical_indication
),
phase_pos                                                           AS ( ---Feb 2nd, 2026: Phase_pos values added 
  SELECT 
    REGEXP_SUBSTR(pha.PHA_UNIQUE_CD, '^(.*)_Phase', 1, 1, 'e', 1)   AS IND_CODE,
    MAX(CASE WHEN pha.PHA_CD = 'Phase 1' THEN pha.PHA_SUCCESS_RATE END) 
	                                                                AS GOV_APPROVED_PHASE_1_POS,
    MAX(CASE WHEN pha.PHA_CD = 'Phase 2A' THEN pha.PHA_SUCCESS_RATE END) 
	                                                                AS GOV_APPROVED_PHASE_2A_POS,
    MAX(CASE WHEN pha.PHA_CD = 'Phase 2B' THEN pha.PHA_SUCCESS_RATE END) 
	                                                                AS GOV_APPROVED_PHASE_2B_POS,
    MAX(CASE WHEN pha.PHA_CD = 'Phase 2' AND pha.PHA_UNIQUE_CD NOT LIKE '%Phase 2A%' 
         AND pha.PHA_UNIQUE_CD NOT LIKE '%Phase 2B%' THEN pha.PHA_SUCCESS_RATE END) 
		                                                            AS GOV_APPROVED_PHASE_2_POS,
    MAX(CASE WHEN pha.PHA_CD = 'Phase 3' THEN pha.PHA_SUCCESS_RATE END) 
	                                                                AS GOV_APPROVED_PHASE_3_POS
  FROM SRV_RND_DF.VW_PHASE pha
  JOIN srv_rnd_df.vw_ref_baseline bas
    ON pha.time_id = bas.time_id
  WHERE bas.bas_desc = 'Live'
    AND pha.PHA_CD IN ('Phase 1', 'Phase 2', 'Phase 2A', 'Phase 2B', 'Phase 3')
  GROUP BY REGEXP_SUBSTR(pha.PHA_UNIQUE_CD, '^(.*)_Phase', 1, 1, 'e', 1)
),

milestone_base                                                                      AS (
    SELECT
        prjmdm_ms.project_code_cd                                                   AS PROJECT_CODE,
        prjmdm_ms.project_phase,wbs.ind_functional_id,
        CASE
            WHEN prjmdm_ms.project_phase IN ('M0-M1', 'M1-M2','M0-M2')
                THEN prjmdm_ms.project_code_cd
            ELSE wbs.ind_functional_id
        END                                                                         AS MILESTONE_SCOPE_CODE,
        tsk.tsk_activity_type                                                       AS MILESTONE_NAME,
        tsk.tsk_planned_finish_dt                                                   AS MILESTONE_PLANNED_FINISH_DT
    FROM srv_rnd_df.vw_task tsk
    INNER JOIN srv_rnd_df.mvw_wbs_hierarchy wbs
        ON wbs.wbs_id = tsk.tsk_wbs_id 
		AND wbs.time_id = tsk.time_id
    INNER JOIN SRV_MDM_RNDMASTERDATA.vw_mdm_project_master prjmdm_ms
        ON prjmdm_ms.project_code_cd = wbs.prj_functional_id

    -- =====================================================
    -- NEW: Join to get indication phase/status for filtering (RT: Feb 6th 2026)
    -- =====================================================
    LEFT JOIN SRV_MDM_RNDMASTERDATA.vw_mdm_project_ind_master indmdm_ms
        ON wbs.ind_functional_id = indmdm_ms.project_ind_code_cd
    -- =====================================================

    INNER JOIN srv_rnd_df.vw_ref_baseline bas
        ON bas.time_id = wbs.time_id 
		AND bas.bas_desc = 'Live'
    WHERE tsk.is_last = TRUE
        AND tsk.tsk_activity_type IN (
            'Target Selection - M0', 'Lead Selection - M1', 'Pre Candidate Selection',
            'Start Development - M2', 'Proof of Commercial Concept', 'Start Ph01',
            'Start Ph02', 'Start Ph2A', 'Start Ph2B', 'Start Ph03',
            'First Submission', 'First Approval', 'Submission', 'Approval','Entry into Portfolio'
        )
        AND prjmdm_ms.project_category IN ('R','D')
        AND prjmdm_ms.project_organization_type IN ('RESEARCH', 'DEVELOPMENT', 'VACCINE')
        AND prjmdm_ms.project_status IN ('Ongoing', 'Completed')
        AND prjmdm_ms.project_phase IN ('M0-M1','M1-M2','M0-M2','Preclinical','Phase 1','Phase 2','Phase 2A','Phase 2B','Phase 3','Regulatory submission','LCM')

        -- =====================================================
        -- NEW: Apply indication filters only when we use indication scope
        -- =====================================================
        AND (
            prjmdm_ms.project_phase IN ('M0-M1', 'M1-M2' ,'M0-M2')
            OR (
                indmdm_ms.project_ind_status IN ('Ongoing', 'Completed')
                AND (
                    indmdm_ms.project_ind_phase IS NULL
                    OR indmdm_ms.project_ind_phase IN (
                        'M0-M1', 'M1-M2', 'M0-M2', 'Preclinical',
                        'Phase 1', 'Phase 2', 'Phase 2A', 'Phase 2B', 'Phase 3',
                        'Regulatory submission', 'LCM'
                    )
                )
            )
        )
        -- =====================================================
),
last_milestone                                                                      AS (
    SELECT
        PROJECT_CODE,
        MILESTONE_SCOPE_CODE,
        MILESTONE_NAME,
        MILESTONE_PLANNED_FINISH_DT  
    FROM (
        SELECT *,
            ROW_NUMBER() OVER (
                PARTITION BY PROJECT_CODE, MILESTONE_SCOPE_CODE
                ORDER BY MILESTONE_PLANNED_FINISH_DT DESC
            )                                                                       AS rn
        FROM milestone_base
        WHERE MILESTONE_PLANNED_FINISH_DT <= CURRENT_DATE()
    )
    WHERE rn = 1
),
next_milestone                                                                      AS (
    SELECT
        PROJECT_CODE,
        MILESTONE_SCOPE_CODE,
        MILESTONE_NAME,
        MILESTONE_PLANNED_FINISH_DT  
    FROM (
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY PROJECT_CODE, MILESTONE_SCOPE_CODE
                               ORDER BY MILESTONE_PLANNED_FINISH_DT ASC)            AS rn
        FROM milestone_base
        WHERE MILESTONE_PLANNED_FINISH_DT > CURRENT_DATE()
    )
    WHERE rn = 1
)

SELECT DISTINCT
    prjmdm.project_code_cd                                                          AS PROJECT_CODE,
    prjmdm.PROJECT_CATEGORY,
    prjmdm.PROJECT_ORGANIZATION,
    prjmdm.project_name_nm                                                          AS PROJECT_NAME,
    prjmdm.project_description_desc                                                 AS PROJECT_DESCRIPTION,
    prjmdm.prj_status                                                               AS PROJECT_STATUS,
    prjmdm.prj_phase                                                                AS PROJECT_PHASE,
    prjmdm.prj_priority                                                             AS PROJECT_PRIORITY,
    prjmdm.prj_innovation_status                                                    AS PROJECT_INNOVATION_STATUS,
    prjmdm.PRJ_DISCO_DEV_LINKED_CODES                                               AS PROJECT_RESEARCH_DEVELOPMENT_LINK,
    CASE
        WHEN prjmdm.project_organization_type = 'VACCINE' THEN 'Vaccines'
        ELSE fou_prj.EN_NM
    END                                                                             AS PROJECT_SANOFI_THERAPEUTIC_AREA,
    prjmdm.prj_inn                                                                  AS ASSET_INN,
    prjmdm.prj_brand_nm                                                             AS ASSET_BRAND_NAME,
    prjmdm.mechanism_of_action                                                      AS ASSET_MECHANISM_OF_ACTION,
    prjmdm.prj_moa_short_nm                                                         AS ASSET_MOA_SHORT_NAME,
    prjmdm.active_substance_type                                                    AS ASSET_ACTIVE_SUBSTANCE_TYPE,
    prjmdm.active_substance_sub_type                                                AS ASSET_ACTIVE_SUBSTANCE_SUBTYPE,
    prjmdm.origin_of_active_substance                                               AS ASSET_ORIGIN_OF_ACTIVE_SUBSTANCE,
    prjmdm.PRJ_PHARMACOLOGICAL_EFFECT                                               AS ASSET_PHARMACOLOGICAL_EFFECT,
    indmdm.project_ind_code_cd                                                      AS INDICATION_UNIQUE_CODE,
    indmdm.ind_lead_flag                                                            AS INDICATION_LEAD_FLAG,
    indmdm.project_ind_description_desc                                             AS INDICATION_LONGNAME,
    indmdm.project_ind_name_nm                                                      AS INDICATION_SHORTNAME,
    indmdm.project_ind_phase                                                        AS INDICATION_PHASE,
    indmdm.clinical_ind                                                             AS INDICATION_CODE_MEDDRA,
    cindmdm.meddra_term                                                             AS INDICATION_NAME_MEDDRA,
    indmdm.project_ind_status                                                       AS INDICATION_STATUS,
    CASE
        WHEN prjmdm.project_organization_type = 'VACCINE' THEN 'Vaccines'
        ELSE fou_ind.EN_NM
    END                                                                             AS INDICATION_SANOFI_THERAPEUTIC_AREA,
    CASE
        WHEN prjmdm.project_organization_type = 'VACCINE' THEN prjmdm.prj_franchise
        ELSE indmdm.ind_v_portfolio_strategic_grouping
    END                                                                             AS INDICATION_SANOFI_SUB_THERAPEUTIC_AREA_FRANCHISE,
    CASE
        WHEN indmdm.ind_pots IS NOT NULL THEN indmdm.ind_pots / 100
        ELSE indmdm.ind_pots
    END                                                                             AS INDICATION_PTRS,
    last_milestone.MILESTONE_NAME                                                   AS LAST_PROJECT_INDICATION_GATE_MILESTONE,
    last_milestone.MILESTONE_PLANNED_FINISH_DT                                      AS LAST_PROJECT_INDICATION_GATE_MILESTONE_DATE,
    next_milestone.MILESTONE_NAME                                                   AS NEXT_PROJECT_INDICATION_GATE_MILESTONE,
    next_milestone.MILESTONE_PLANNED_FINISH_DT                                      AS NEXT_PROJECT_INDICATION_GATE_MILESTONE_DATE,
	  phase_pos.GOV_APPROVED_PHASE_1_POS                                AS GOV_APPROVED_PHASE_1_POS, -- Jan 27th 2026, Rohit T: adding Phase level POS for Phase 1, Phase 2a, Phase 2b, Phase 2, Phase 3
  phase_pos.GOV_APPROVED_PHASE_2A_POS                               AS GOV_APPROVED_PHASE_2A_POS,
  phase_pos.GOV_APPROVED_PHASE_2B_POS                               AS GOV_APPROVED_PHASE_2B_POS,
  phase_pos.GOV_APPROVED_PHASE_2_POS                                AS GOV_APPROVED_PHASE_2_POS,
  phase_pos.GOV_APPROVED_PHASE_3_POS                                AS GOV_APPROVED_PHASE_3_POS,
	prjmdm.time_id                                                                  AS LAST_REFRESH_DATE
FROM prjmdm
JOIN indmdm
    ON prjmdm.project_code_cd = indmdm.indmdm_project_code
LEFT JOIN fou fou_prj
    ON prjmdm.prj_responsability_fou_fk = fou_prj.rdm_code_cd
LEFT JOIN fou fou_ind
    ON indmdm.ind_fou_fk = fou_ind.rdm_code_cd
LEFT JOIN cindmdm
    ON indmdm.clinical_ind = cindmdm.rdm_code_cd
LEFT JOIN phase_pos
  ON indmdm.project_ind_code_cd = phase_pos.IND_CODE
LEFT JOIN last_milestone
    ON prjmdm.project_code_cd = last_milestone.PROJECT_CODE
    AND (
        ( prjmdm.prj_phase IN ('M0-M1', 'M1-M2','M0-M2')
            AND last_milestone.MILESTONE_SCOPE_CODE = prjmdm.project_code_cd
        )
        OR (prjmdm.prj_phase NOT IN ('M0-M1', 'M1-M2','M0-M2')
            AND indmdm.project_ind_status IN ('Ongoing', 'Completed')
            AND last_milestone.MILESTONE_SCOPE_CODE = indmdm.project_ind_code_cd
        )
    )
LEFT JOIN next_milestone
    ON prjmdm.project_code_cd = next_milestone.PROJECT_CODE
    AND (
        ( prjmdm.prj_phase IN ('M0-M1', 'M1-M2','M0-M2')
            AND next_milestone.MILESTONE_SCOPE_CODE = prjmdm.project_code_cd
        )
        OR ( prjmdm.prj_phase NOT IN ('M0-M1', 'M1-M2','M0-M2')
            AND indmdm.project_ind_status IN ('Ongoing', 'Completed')
            AND next_milestone.MILESTONE_SCOPE_CODE = indmdm.project_ind_code_cd
        )
    )
  );

