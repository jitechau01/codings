
  create or replace   view working.public.vw_project_tcp
  
  
  
  
  as (
    with vw_project_tcp as
   (
    SELECT 
		TCP_PROF_ID    AS TCP_ID,
		"Project Code" AS PROJECT_CODE,
		"Project Name" AS PROJECT_NAME,
    CASE 
        WHEN "Title" = 'Potential Indications & FIC / BIC Potential' 
        THEN "Attribute Name"
        ELSE "Title"
        END            AS TCP_CHARACTERISTIC,
		"Comments"     AS TCP_CHARACTERISTIC_VALUE,
		"Status"       AS TCP_STATUS,
		"Created By"   AS TCP_CREATED_BY,
		"Modified By"  AS TCP_MODIFIED_BY,
		"Created"      AS TCP_CREATED_DATE,
		"Modified"     AS TCP_MODIFIED_DATE
	FROM 
		CRDH_DEA_IPORT_REPORTING.PRTFL_TCP_PROFILE
	WHERE 
		     ("Status"  LIKE 'Published%'
			OR "Status" LIKE 'Draft%')
	ORDER BY 
		TCP_PROF_ID
        )
SELECT * FROM vw_project_tcp
  );

