
  create or replace   view working.public.vw_project_tvp
  
  
  
  
  as (
    WITH AGGREGATED_TVP AS (
        SELECT
            "Project Code",
            INDICATION,
            LISTAGG(DISTINCT CASE WHEN TITLE = 'For' THEN "Comments" END, '; ') 
			                          AS TVP_POPULATIONS_OF_INTEREST,
            LISTAGG(DISTINCT CASE WHEN TITLE = 'Who' THEN "Comments" END, '; ') 
			                          AS TVP_NEED,
            LISTAGG(DISTINCT CASE WHEN TITLE = 'Our product is' AND "Attribute Name" = 'Versus current SoC' THEN "Comments" END, '; ') 
			                          AS TVP_COMPETITIVE_POSITIONING_CURRENT_SOC,
            LISTAGG(DISTINCT CASE WHEN TITLE = 'Our product is' AND "Attribute Name" = 'Versus future SoC/Main Competitors' THEN "Comments" END, '; ') 
			                          AS TVP_COMPETITIVE_POSITIONING_FUTURE_SOC_COMPETITORS,
            LISTAGG(DISTINCT CASE WHEN TITLE = 'That will' AND "Attribute Name" = 'Prescribers' THEN "Comments" END, '; ') 
			                          AS TVP_VALUE_TO_PRESCRIBERS,
            LISTAGG(DISTINCT CASE WHEN TITLE = 'That will' AND "Attribute Name" = 'Patients' THEN "Comments" END, '; ') 
			                          AS TVP_VALUE_TO_PATIENTS,
            LISTAGG(DISTINCT CASE WHEN TITLE = 'That will' AND "Attribute Name" = 'Payers' THEN "Comments" END, '; ') 
			                          AS TVP_VALUE_TO_PAYERS,
            LISTAGG(DISTINCT STATUS, ', ') WITHIN GROUP (ORDER BY STATUS) 
			                          AS TVP_STATUS,
            LISTAGG(DISTINCT TVP_PROF_ID, ',') WITHIN GROUP (ORDER BY TVP_PROF_ID) 
			                          AS TVP_SOURCE_RECORD_IDS,
            CASE 
                WHEN COUNT(DISTINCT "Created By") > 1 
                    THEN LISTAGG(DISTINCT CONCAT("Created By", ' (', TO_VARCHAR(CREATED, 'YYYY-MM-DD'), ')'), ', ')
                ELSE MAX("Created By")
            END                       AS CREATED_BY,
            CASE
                WHEN COUNT(DISTINCT "Modified By") > 1 
                    THEN LISTAGG(DISTINCT CONCAT("Modified By", ' (', TO_VARCHAR(MODIFIED, 'YYYY-MM-DD'), ')'), ', ')
                ELSE MAX("Modified By")
            END                        AS MODIFIED_BY,
            MIN(CREATED)               AS CREATED_DATE,
            MAX(MODIFIED)              AS MODIFIED_DATE
        FROM CRDH_DEA_IPORT_REPORTING.PRTFL_TVP_PROFILE
        WHERE STATUS IN ('Published', 'Draft', 'Publish') 
        GROUP BY "Project Code",
        		INDICATION
    )
    SELECT
        "Project Code"                 AS PROJECT_CODE,
        INDICATION                     AS INDICATION_UNIQUE_CODE,
        TVP_POPULATIONS_OF_INTEREST,
        TVP_NEED,
        TVP_COMPETITIVE_POSITIONING_CURRENT_SOC,
        TVP_COMPETITIVE_POSITIONING_FUTURE_SOC_COMPETITORS,
        TVP_VALUE_TO_PRESCRIBERS,
        TVP_VALUE_TO_PATIENTS,
        TVP_VALUE_TO_PAYERS,
        TVP_STATUS,
        TVP_SOURCE_RECORD_IDS,
        CREATED_BY,
        MODIFIED_BY,
        CREATED_DATE,
        MODIFIED_DATE
    FROM AGGREGATED_TVP
    ORDER BY 
        INDICATION_UNIQUE_CODE,
        PROJECT_CODE
  );

