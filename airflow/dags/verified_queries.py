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
    # },
    # {
    # "name": "What is the current distribution of research projects across unique therapeutic indications and medical conditions in our pharmaceutical portfolio?",
    # "question": "What is the current distribution of research projects across unique therapeutic indications and medical conditions in our pharmaceutical portfolio?",
    # "sql": 
    #     """SELECT
    #     COUNT(indication_unique_code, project_code) AS count_indication_unique_code_project_code,
    #     COUNT(
    #         DISTINCT HASH(indication_unique_code, project_code)
    #     ) AS distinct_indication_unique_code_project_code,
    #     COUNT(project_code) AS count_project_code,
    #     COUNT(DISTINCT project_code) AS distinct_project_code,
    #     COUNT(indication_code_meddra) AS count_indication_code_meddra,
    #     COUNT(DISTINCT indication_code_meddra) AS distinct_indication_code_meddra
    #     FROM
    #     vw_project_indication_flat"""
    # },
    # {
    # "name": "How many unique project-indication combinations exist in our pharmaceutical R&D portfolio?",
    # "question": "How many unique project-indication combinations exist in our pharmaceutical R&D portfolio?",
    # "sql":  """SELECT
    #             COUNT(indication_unique_code, project_code) AS count_indication_unique_code_project_code,
    #             COUNT(DISTINCT HASH(indication_unique_code, project_code)) 
    #             AS distinct_indication_unique_code_project_code
    #         FROM
    #             vw_project_team_member """ 
    # },
    # {
    # "name": "Calculate the product (multiplication) of all non-null GOV_APPROVED_PHASE_1_POS values across all records in the project indication flat table?",
    # "question": "Calculate the product (multiplication) of all non-null GOV_APPROVED_PHASE_1_POS values across all records in the project indication flat table?",
    # "sql":  """SELECT
    #     EXP(SUM(LN(NULLIF(gov_approved_phase_1_pos, 0)))) AS product_gov_approved_phase_1_pos
    #   FROM
    #     vw_project_indication_flat
    #   WHERE
    #     NOT gov_approved_phase_1_pos IS NULL
    #     AND gov_approved_phase_1_pos <> 0 """ 
    # },
    #  {
    # "name": "Calculate the total sum of GOV_APPROVED_PHASE_1_POS across all records in the entire available time period?",
    # "question": "Calculate the total sum of GOV_APPROVED_PHASE_1_POS across all records in the entire available time period?",
    # "sql":  """SELECT
    #     MIN(project_code) AS first_project,
    #     MAX(project_code) AS last_project,
    #     SUM(gov_approved_phase_1_pos) AS total_gov_approved_phase_1_pos
    #   FROM
    #     vw_project_indication_flat """
    # },
    #   {
    # "name": "How many unique project-indication combinations do we have in our pharmaceutical R&D portfolio?",
    # "question": "How many unique project-indication combinations do we have in our pharmaceutical R&D portfolio?",
    # "sql":  """SELECT
    #     COUNT(indication_unique_code, project_code) AS count_indication_unique_code_project_code,
    #     COUNT(
    #       DISTINCT HASH(indication_unique_code, project_code)
    #     ) AS distinct_indication_unique_code_project_code
    #   FROM
    #     vw_project_indication_tpp"""
    # },
    #    {
    # "name": "How many therapeutic value proposition assessments have we conducted in total, and how many of these are unique combinations of indications and projects?",
    # "question": "CaHow many therapeutic value proposition assessments have we conducted in total, and how many of these are unique combinations of indications and projects?",
    # "sql":  """SELECT
    #     COUNT(indication_unique_code, project_code) AS count_indication_unique_code_project_code,
    #     COUNT(
    #       DISTINCT HASH(indication_unique_code, project_code)
    #     ) AS distinct_indication_unique_code_project_code
    #   FROM
    #     vw_project_tvp """ 
    # },
    # {
    # "name": "What is the current scope of our pharmaceutical research portfolio in terms of total projects, therapeutic indications, and unique project-indication combinations?",
    # "question": "What is the current scope of our pharmaceutical research portfolio in terms of total projects, therapeutic indications, and unique project-indication combinations?",
    # "sql":  """SELECT
    #     COUNT(DISTINCT project_code) AS unique_projects,
    #     COUNT(DISTINCT indication_unique_code) AS unique_indications,
    #     COUNT(
    #       DISTINCT HASH(project_code, indication_unique_code)
    #     ) AS unique_project_indication_pairs
    #   FROM
    #     vw_project_indication_flat """ 
    # }
    ]