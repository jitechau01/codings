verified_queries =[
    {
    "name": "What is the total number of unique therapeutic value proposition assessments we have conducted, and what is their date range?",
    "question": "What is the total number of unique therapeutic value proposition assessments we have conducted, and what is their date range?",
    "sql": 
        """SELECT
            COUNT(
            DISTINCT HASH(project_code, indication_unique_code)
            ) AS unique_tvp_assessments,
            MIN(created_date) AS earliest_assessment_date,
            MAX(created_date) AS latest_assessment_date
        FROM
            vw_project_tvp"""
    },
    {
    "name": "What is the current distribution of research projects across unique therapeutic indications and medical conditions in our pharmaceutical portfolio?",
    "question": "What is the current distribution of research projects across unique therapeutic indications and medical conditions in our pharmaceutical portfolio?",
    "sql": 
        """SELECT
        COUNT(indication_unique_code, project_code) AS count_indication_unique_code_project_code,
        COUNT(
            DISTINCT HASH(indication_unique_code, project_code)
        ) AS distinct_indication_unique_code_project_code,
        COUNT(project_code) AS count_project_code,
        COUNT(DISTINCT project_code) AS distinct_project_code,
        COUNT(indication_code_meddra) AS count_indication_code_meddra,
        COUNT(DISTINCT indication_code_meddra) AS distinct_indication_code_meddra
        FROM
        vw_project_indication_flat"""
    },
    {
    "name": "How many unique project-indication combinations exist in our pharmaceutical R&D portfolio?",
    "question": "How many unique project-indication combinations exist in our pharmaceutical R&D portfolio?",
    "sql":  """SELECT
                COUNT(indication_unique_code, project_code) AS count_indication_unique_code_project_code,
                COUNT(DISTINCT HASH(indication_unique_code, project_code)) 
                AS distinct_indication_unique_code_project_code
            FROM
                vw_project_team_member """ #,
    # "use_as_onboarding_question": "false"
    # "verified_by": "DEV_USER",
    # "verified_at": "1773042395"
    }
    ]