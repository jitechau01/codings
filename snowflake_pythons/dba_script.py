from __con import _conn
from __con_adam import _conn_adam

schema_list=['landing','crdh_dea_iport_reporting', 'dp_rdportfolio360', 'semantic', 'srv_mdm_rndmasterdata', 'srv_rnd_df', 'stg_manual_inputs']

def accountadmin_task():
    cur=_conn()
    cur.execute("use role accountadmin")
    #print(cur.execute("select current_role()").fetchall())
    try:
        print("\n-------------Role & user Creation Starts-----------------------")
        result=cur.execute("create role if not exists lead")
        status=result.fetchone()
        
        if status:
            message=status[0]
            message=message.lower()
            if "already exists" in message:
                print("role lead already exists, skipped creation")
            elif "successfully created" in message:
                print("role lead successfully created")
                cur.execute("grant role sysadmin to role lead")
                cur.execute("grant role securityadmin to role lead")   
                cur.execute("grant usage on warehouse compute_wh to role lead")  
    except Exception as e:
        print("Error:{e}")
        #Handle error  
         
    try:        
        result=cur.execute("create user if not exists adam")
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print("user adam successfully created")
                cur.execute("grant role lead to user adam")
            elif "already exists" in message:
                print("user adam already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error    
def create_db_schemas():
    cur=_conn_adam()
    cur.execute("use role lead")
    #print(cur.execute("select current_role()").fetchall())
    # cur.execute("drop database if exists sales")
    try:
        print("\n-------------database & schema Creation Starts-------------------")
        result = cur.execute("CREATE DATABASE IF NOT EXISTS sales")
        
        status = result.fetchone()
        
        if status:
            message = status[0]
            
            if "successfully created" in message.lower():
                print("Database Sales created successfully, proceeding for schema Creations")
                for schema in schema_list:
                    cur.execute(f"create schema if not exists sales.{schema} ")
                    status = cur.fetchone()
                    if status:
                        message = status[0]
                        if "successfully created" in message.lower():
                            print(f"Schema sales.{schema} created successfully")
                        elif "already exists" in message.lower():
                            print(f"Schema sales.{schema} already exists, skipped creation")

            elif "already exists" in message.lower():
                print("Database Sales already exists, skipped creation, proceeding for Schema Creations")
                for schema in schema_list:
                    cur.execute(f"create schema if not exists sales.{schema} ")
                    status = cur.fetchone()
                    if status:
                        message = status[0]
                        if "successfully created" in message.lower():
                            print(f"Schema sales.{schema} created successfully")
                        elif "already exists" in message.lower():
                            print(f"Schema sales.{schema} already exists, skipped creation")
        
    except Exception as e:
        print(f"Error: {e}")
        # Handle error
def create_tables():
    cur=_conn_adam()
    cur.execute("""use schema sales.landing""")
    print("\n-----------Table Creation Starts-------------------")
    try: 
        result=cur.execute("""create table if not exists ICD10_MEDDRA_MAPPING (
        ICD10_CHAPTER_NUMBER_2019_INTL_CORE_VER VARCHAR(15),
        ICD10_CHAPTER_2019_INTL_CORE_VER VARCHAR(512),
        ICD10_CODE_2019_INTL_CORE_VER VARCHAR(15),
        ICD10_TERM_2019_INTL_CORE_VER VARCHAR(512),
        MAPPED_MEDDRA_LLT VARCHAR(512),
        MAPPED_MEDDRA_LLT_CODE VARCHAR(15),
        MAP_ATTRIBUTE VARCHAR(128),
        MEDDRA_PT VARCHAR(512),
        MEDDRA_PT_CODE VARCHAR(15),
        MEDDRA_VER VARCHAR(15))
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table ICD10_MEDDRA_MAPPING successfully created")
                elif "already exists" in message:
                    print("ICD10_MEDDRA_MAPPING Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
        
    try:
        result=cur.execute("""create table if not exists INDICATION (
            TIME_ID VARCHAR(255),
            IND_WBS_ID VARCHAR(16777216),
            IND_UNIQUE_CD VARCHAR(255),
            HUB_START_DT TIMESTAMP_NTZ(0),
            IND_POS_TO_POCC FLOAT,
            IND_POTS FLOAT,
            IND_SR_POCC FLOAT,
            IND_NEXT_PHASE_SUCCESS_RATE FLOAT,
            IND_NEXT_PHASE_PRP FLOAT,
            IND_DEV_OBJECTIVE VARCHAR(5000),
            IND_FORMULATION VARCHAR(255),
            IND_NUMBER VARCHAR(255),
            IND_PHASE VARCHAR(255),
            IND_PRIORITY VARCHAR(255),
            IND_STATUS VARCHAR(255),
            IND_STATUS_DETAILED VARCHAR(255),
            IND_THP_FK VARCHAR(255),
            IND_CD VARCHAR(255),
            IND_ACTUAL_START_DT DATE,
            IND_PLANNED_START_DT DATE,
            IND_ACTUAL_FINISH_DT DATE,
            IND_PLANNED_FINISH_DT DATE,
            IND_ADMIN_ROUTE VARCHAR(255),
            IND_FOU_FK VARCHAR(255),
            IND_DESC VARCHAR(5000),
            IND_PHARMA_FLAG BOOLEAN,
            IND_VACCIN_FLAG BOOLEAN,
            IND_LEAD_FLAG BOOLEAN,
            IND_NEXT_GNG_DT DATE,
            IND_NEXT_PHASE VARCHAR(255),
            IND_NEXT_PHASE_START_DT DATE,
            IND_STOPPED_DT DATE,
            MD5 VARCHAR(255),
            CREATE_TS TIMESTAMP_NTZ(9),
            UPDATE_TS TIMESTAMP_NTZ(9),
            CREATED_BY VARCHAR(255),
            UPDATED_BY VARCHAR(255),
            IND_ONB NUMBER(28,0),
            IND_V_COST_LAUNCH NUMBER(28,0),
            IND_V_CUSTO_PRJ_FLAG BOOLEAN,
            IND_V_INC_YEAR_CUMUL FLOAT,
            IND_V_PEAK_SALES NUMBER(28,0),
            IND_V_IND_DRIVER VARCHAR(255),
            IND_V_IND_OBJ VARCHAR(5000),
            IND_V_NPV NUMBER(28,0),
            IND_V_PRIO_COMMENT VARCHAR(255),
            IND_V_REASON_STOP VARCHAR(255),
            IND_V_EXP_SYSTEM VARCHAR(255),
            IND_V_SC_SHORT_NAME VARCHAR(255),
            IND_V_SC_ASSUMPTION VARCHAR(255),
            IND_V_MAIN_CHANGES VARCHAR(255),
            IND_V_MARKET_POSITION VARCHAR(255),
            IND_V_MARKET_RATIONAL VARCHAR(5000),
            IND_V_BUS_SUSTAINABILITY_FLAG BOOLEAN,
            IND_V_COMMITMENT BOOLEAN,
            IND_V_COMM_OPPORTUNITY VARCHAR(255),
            IND_V_VELOCITY VARCHAR(255),
            IND_SHORTNAME VARCHAR(255),
            IND_V_PRIORITY NUMBER(28,0),
            IND_V_SITE VARCHAR(255),
            IND_V_FINANCIAL_CATEGORY VARCHAR(255),
            IND_V_PRODUCT_CD_SYNONYM VARCHAR(255),
            IND_V_ALL_ROOT_PRODUCT_CODES VARCHAR(255),
            IND_REPORTING VARCHAR(255),
            IND_BENCHMARK_FORMULATION VARCHAR(255),
            IND_V_PORTFOLIO_STRATEGIC_GROUPING VARCHAR(255),
            IND_V_COMMITMENT_PIVOTAL VARCHAR(255),
            IND_V_NBR_ANTIGEN FLOAT,
            IND_V_NBR_COMMITMENT_PIVOTAL FLOAT,
            IND_TERMINATION_REASON VARCHAR(255),
            IND_FREE_FIELD_PROJECT_PPR NUMBER(28,0),
            IND_PFM VARCHAR(4000),
            IND_PFM_DESC VARCHAR(4000),
            IND_ECODES VARCHAR(4000),
            IND_ECODESIGN_STATUS VARCHAR(255),
            IND_CLIMATE_CHANGE_IMPACT VARCHAR(255),
            START_DT TIMESTAMP_NTZ(9),
            END_DT TIMESTAMP_NTZ(9),
            IS_LAST BOOLEAN)
        """)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print("Table INDICATION successfully created")
            elif "already exists" in message:
                print("INDICATION Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    
    try:
        result=cur.execute("""create table if not exists MDM_CLINICAL_INDICATION (
            RDM_NAME_NM VARCHAR(256),
            RDM_CODE_CD VARCHAR(256),
            MEDDRA_TERM VARCHAR(256),
            ACRONYM VARCHAR(256),
            ISACTIVE VARCHAR(256),
            CREATED_BY VARCHAR(256),
            CREATE_DATE_TS TIMESTAMP_NTZ(9),
            UPDATED_BY VARCHAR(256),
            LAST_UPDATE_DATE_TS TIMESTAMP_NTZ(9),
            SOURCE_SYSTEM VARCHAR(256))
        """)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print("Table MDM_CLINICAL_INDICATION successfully created")
            elif "already exists" in message:
                print("MDM_CLINICAL_INDICATION Table already exists, skipped creation")
    except Exception as e:
            print("Error:{e}")
            #Handle error

    try:
        result=cur.execute("""create table if not exists MDM_FINANCIAL_ORGANIZATION_UNIT (
            RDM_CODE_CD VARCHAR(256),
            RDM_NAME_NM VARCHAR(256),
            TYPE VARCHAR(256),
            EN_NM VARCHAR(256),
            PARENT_CODE_CD VARCHAR(256),
            LEVEL2TYPE VARCHAR(256),
            ISACTIVE VARCHAR(256),
            CREATED_BY VARCHAR(256),
            CREATE_DATE_TS TIMESTAMP_NTZ(9),
            UPDATED_BY VARCHAR(256),
            LAST_UPDATE_DATE_TS TIMESTAMP_NTZ(9),
            SOURCE_SYSTEM VARCHAR(256))
        """)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print("Table MDM_FINANCIAL_ORGANIZATION_UNIT successfully created")
            elif "already exists" in message:
                print("MDM_FINANCIAL_ORGANIZATION_UNIT Table already exists, skipped creation")
    except Exception as e:
            print("Error:{e}")
            #Handle error
    
    try:      
        result=cur.execute("""create table if not exists MDM_PROJECT_IND_MASTER (
            ID NUMBER(38,0),
            SOURCE_PKEY VARCHAR(256),
            BUSINESS_ID VARCHAR(256),
            PROJECT_IND_CODE_CD VARCHAR(256),
            PROJECT_IND_NAME_NM VARCHAR(256),
            PROJECT_IND_DESCRIPTION_DESC VARCHAR(256),
            PROJECT_IND_RESPONSIBLE VARCHAR(256),
            PROJECT_IND_STATUS VARCHAR(256),
            PROJECT_IND_STATUS_DETAILED VARCHAR(256),
            CLINICAL_IND VARCHAR(256),
            MEDICAL_THERAPEUTIC_AREA VARCHAR(256),
            SOURCE_SYSTEM VARCHAR(256),
            CREATIONDATE_DT TIMESTAMP_NTZ(9),
            LASTUPDATEDATE_DT TIMESTAMP_NTZ(9),
            CREATEDBY VARCHAR(256),
            UPDATEDBY VARCHAR(256),
            PROJECT_IND_PHASE VARCHAR(256),
            STATE VARCHAR(50))
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table MDM_PROJECT_IND_MASTER successfully created")
                elif "already exists" in message:
                    print("MDM_PROJECT_IND_MASTER Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error

    try:
        result=cur.execute("""create table if not exists MDM_PROJECT_MASTER (
                ID NUMBER(38,0),
                SOURCE_PKEY VARCHAR(255),
                BUSINESS_ID VARCHAR(255),
                PROJECT_CODE_CD VARCHAR(255),
                PROJECT_RESPONSIBLE VARCHAR(255),
                PROJECT_ORGANIZATION_TYPE VARCHAR(255),
                PROJECT_TYPE VARCHAR(50),
                PROJECT_SUBTYPE VARCHAR(50),
                PROJECT_NAME_NM VARCHAR(255),
                PROJECT_DESCRIPTION_DESC VARCHAR(4000),
                PROJECT_CATEGORY VARCHAR(1),
                PROJECT_STATUS VARCHAR(30),
                PROJECT_STATUS_DETAILED VARCHAR(30),
                PROJECT_PHASE VARCHAR(50),
                MECHANISM_OF_ACTION VARCHAR(256),
                ACTIVE_SUBSTANCE_TYPE VARCHAR(30),
                ACTIVE_SUBSTANCE_SUB_TYPE VARCHAR(50),
                ORIGIN_OF_ACTIVE_SUBSTANCE VARCHAR(30),
                ORIGIN_COMPANY_OF_ACTIVE_SUBSTANCE VARCHAR(255),
                EXTERNAL_ACTIVE_SUBSTANCE_CODE VARCHAR(255),
                DATE_OF_AGREEMENT TIMESTAMP_NTZ(9),
                BRAND_NAME_NM VARCHAR(255),
                INN VARCHAR(255),
                RA_CODE VARCHAR(50),
                ADDITIONAL_PROJECT_INFORMATION VARCHAR(1000),
                RESEARCH_PROJECT_TARGET VARCHAR(256),
                RW_CLUSTER VARCHAR(256),
                SCREENING_ORIENTATION VARCHAR(60),
                SCREEN_TYPE VARCHAR(60),
                TARGET_RATIONALE VARCHAR(2500),
                PROJECT_GLOBAL_OBJECTIVE VARCHAR(4000),
                SOURCE_SYSTEM VARCHAR(256),
                CREATIONDATE_DT TIMESTAMP_NTZ(9),
                LASTUPDATEDATE_DT TIMESTAMP_NTZ(9),
                CREATEDBY VARCHAR(256),
                UPDATEDBY VARCHAR(256),
                SOURCE_OF_ORIGIN VARCHAR(10),
                STATE VARCHAR(50))
            """)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print("Table MDM_PROJECT_MASTER successfully created")
            elif "already exists" in message:
                print("MDM_PROJECT_MASTER Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error

    try:
        result=cur.execute("""create table if not exists MEDDRA_SNOMED_CT_MAPPING (
            MEDDRA_LLT_CODE VARCHAR(15),
            MEDDRA_LLT VARCHAR(512),
            SNOMED_CT_CODE VARCHAR(50),
            SNOMED_CT_FSN VARCHAR(512))
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table MEDDRA_SNOMED_CT_MAPPING successfully created")
                elif "already exists" in message:
                    print("MEDDRA_SNOMED_CT_MAPPING Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error

    try:
        result=cur.execute("""create table if not exists PHASE (
            TIME_ID VARCHAR(255),
            PHA_WBS_ID VARCHAR(255),
            PHA_UNIQUE_CD VARCHAR(255),
            HUB_START_DT TIMESTAMP_NTZ(0),
            PHA_SUCCESS_RATE FLOAT,
            PHA_PRP NUMBER(28,0),
            PHA_CD VARCHAR(255),
            PHA_WEIGHTING FLOAT,
            PHA_PLANNED_START_DT DATE,
            PHA_PLANNED_FINISH_DT DATE,
            PHA_ACTUAL_START_DT DATE,
            PHA_ACTUAL_FINISH_DT DATE,
            PHA_ONB NUMBER(28,0),
            PHA_ORDER_NM VARCHAR(255),
            PHA_DESC VARCHAR(5000),
            PHA_CURRENT_PHASE_FLAG BOOLEAN,
            PHA_PHARMA_FLAG BOOLEAN,
            PHA_VACCIN_FLAG BOOLEAN,
            PHA_V_REPORT_PHASE_FLG BOOLEAN,
            PHA_V_SUCCES_RATE VARCHAR(255),
            PHA_V_SUCCES_RATE_APPROVAL_DT DATE,
            PHA_V_TYPE VARCHAR(255),
            MD5 VARCHAR(255),
            CREATE_DT TIMESTAMP_NTZ(0),
            UPDATE_DT TIMESTAMP_NTZ(0),
            CREATED_BY VARCHAR(255),
            UPDATED_BY VARCHAR(255),
            PHA_V_YEARLY_START_DT DATE,
            PHA_V_YEARLY_FINISH_DT DATE,
            PHA_BUDGETED BOOLEAN,
            YEARLY_BASELINE_FINISH_DATE_2014 DATE,
            YEARLY_BASELINE_START_DATE_2014 DATE,
            YEARLY_BASELINE_FINISH_DATE_2015 DATE,
            YEARLY_BASELINE_START_DATE_2015 DATE,
            YEARLY_BASELINE_FINISH_DATE_2016 DATE,
            YEARLY_BASELINE_START_DATE_2016 DATE,
            YEARLY_BASELINE_FINISH_DATE_2017 DATE,
            YEARLY_BASELINE_START_DATE_2017 DATE,
            YEARLY_BASELINE_START_DATE_2018 DATE,
            YEARLY_BASELINE_FINISH_DATE_2018 DATE,
            YEARLY_BASELINE_START_DATE_2019 DATE,
            YEARLY_BASELINE_FINISH_DATE_2019 DATE,
            YEARLY_BASELINE_START_DATE_2020 DATE,
            YEARLY_BASELINE_FINISH_DATE_2020 DATE,
            START_DT TIMESTAMP_NTZ(0),
            END_DT TIMESTAMP_NTZ(9),
            IS_LAST BOOLEAN)
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table PHASE successfully created")
                elif "already exists" in message:
                    print("PHASE Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:           
        result=cur.execute("""create table if not exists PROJECT (
            TIME_ID VARCHAR(255),
            PRJ_WBS_ID VARCHAR(255),
            PRJ_CD VARCHAR(255),
            HUB_START_DT TIMESTAMP_NTZ(0),
            PRJ_ONB NUMBER(28,0),
            PRJ_NM VARCHAR(255),
            PRJ_DESC VARCHAR(5000),
            PRJ_COM_TERMINATION VARCHAR(255),
            PRJ_TERMINATION_REASON VARCHAR(255),
            PRJ_ADMINISTRATION_ROUTE VARCHAR(255),
            PRJ_ANTIGEN VARCHAR(255),
            PRJ_BRAND_NM VARCHAR(255),
            PRJ_CMC_PORTFOLIO VARCHAR(255),
            PRJ_CODEV_PARTNER VARCHAR(255),
            PRJ_PIPELINE_COMMENT VARCHAR(255),
            PRJ_CREATION_DT TIMESTAMP_NTZ(9),
            PRJ_CUSTOMIZED_FLAG BOOLEAN,
            PRJ_COST_LAUNCH_RELATED_DT DATE,
            PRJ_ACQUISITION_DT DATE,
            PRJ_COMPLETION_DT DATE,
            PRJ_TERMINATION_DT DATE,
            PRJ_DEV_DEVICE_FLAG BOOLEAN,
            PRJ_DISCO_DEV_LINKED_CODES VARCHAR(255),
            PRJ_ENTERING_PREDEV_DT DATE,
            PRJ_ENTERING_DEV_DT DATE,
            PRJ_EXITING_DEV_DT DATE,
            PRJ_EXITING_PREDEV_DT DATE,
            PRJ_EXP_GENERIC_ENTRY_DT DATE,
            PRJ_FRANCHISE VARCHAR(255),
            PRJ_FUNDING_ZONE VARCHAR(255),
            PRJ_GEOGRAPHICAL_TARGET VARCHAR(255),
            PRJ_HUB_OWNER VARCHAR(255),
            PRJ_INN VARCHAR(255),
            PRJ_INNOVATION_STATUS VARCHAR(255),
            PRJ_MOA VARCHAR(255),
            PRJ_MOLECULE_SUBTYPE VARCHAR(255),
            PRJ_MOLECULE_TYPE VARCHAR(255),
            PRJ_OBJECTIVE VARCHAR(5000),
            PRJ_PARTNER_NM VARCHAR(255),
            PRJ_NME_ORIGIN VARCHAR(255),
            PRJ_OWNER VARCHAR(255),
            PRJ_PATENT_INFORMATION VARCHAR(255),
            PRJ_PATHOGEN VARCHAR(255),
            PRJ_V_PPP_PRJ_LEADER VARCHAR(255),
            PRJ_V_PPP_PRJ_MANAGER VARCHAR(255),
            PRJ_PLANNED_FINISH_DT DATE,
            PRJ_PLANNED_START_DT DATE,
            PRJ_TPR_FK NUMBER(28,0),
            PRJ_PROJECT_LEADER_ENTRY VARCHAR(255),
            PRJ_PHASE VARCHAR(255),
            PRJ_EBINDER_LINK VARCHAR(255),
            PRJ_SITE VARCHAR(255),
            PRJ_STATUS VARCHAR(255),
            PRJ_STATUS_DETAILED VARCHAR(255),
            PRJ_SUBCATEGORY VARCHAR(255),
            PRJ_RESPONSABILITY_FOU_FK VARCHAR(255),
            PRJ_ROOT_PRODUCT VARCHAR(255),
            PRJ_PUBLIC_FUNDING_ORG VARCHAR(255),
            PRJ_RECOMMANNDATION VARCHAR(255),
            PRJ_STAGE VARCHAR(255),
            PRJ_VACCIN_CATEGORY VARCHAR(255),
            PRJ_STATE VARCHAR(255),
            PRJ_VACCIN_TYPE VARCHAR(255),
            PRJ_VARIANCE_ANALYSIS VARCHAR(255),
            PRJ_APPROACH_PHASE_AT_PRIO VARCHAR(255),
            PRJ_PROJECT_MANAGER VARCHAR(255),
            PRJ_PARTNER_PRODUCT_CD VARCHAR(255),
            PRJ_CLUSTER_CD VARCHAR(255),
            PRJ_CLUSTER_DESC VARCHAR(255),
            PRJ_PORTFOLIO_MAIN VARCHAR(255),
            PRJ_PORTFOLIO VARCHAR(255),
            PRJ_DATABASE VARCHAR(255),
            PRJ_PHARMA_FLAG BOOLEAN,
            PRJ_VACCIN_FLAG BOOLEAN,
            PRJ_PRIORITY VARCHAR(255),
            PRJ_DEV_ENTRY_DT DATE,
            PRJ_FIRST_APPROACH_DT DATE,
            PRJ_NEXT_GNG_DT DATE,
            PRJ_NEXT_GNG_CD VARCHAR(255),
            PRJ_PERM_PROJECT_FLAG BOOLEAN,
            PRJ_NAME_EXT_SOURCE VARCHAR(255),
            PRJ_V_GLOBAL_PRJ_HEAD VARCHAR(255),
            PRJ_V_TARGET_POPULATION VARCHAR(255),
            PRJ_V_SHINE_PRJ_CD VARCHAR(255),
            PRJ_V_PRIORITY NUMBER(28,0),
            PRJ_MOLECULE_TYPE_CD VARCHAR(255),
            PRJ_MOLECULE_SUBTYPE_CD VARCHAR(255),
            PRJ_V_APAO_PRJ_LIST VARCHAR(255),
            PRJ_V_APAO_PRJ_FLAG BOOLEAN,
            PRJ_V_KHM VARCHAR(255),
            PRJ_MOA_SHORT_NM VARCHAR(255),
            MD5 VARCHAR(255),
            CREATE_TS TIMESTAMP_NTZ(9),
            UPDTED_TS TIMESTAMP_NTZ(9),
            PRJ_V_FINANCIAL_CATEGORY VARCHAR(255),
            PRJ_PHARMACOLOGICAL_EFFECT VARCHAR(255),
            PRJ_CYCLE VARCHAR(255),
            PRJ_V_PRODUCT_CD_SYNONYM VARCHAR(255),
            PRJ_V_ALL_PRODUCT_CODES VARCHAR(255),
            PRJ_REPORTING VARCHAR(255),
            PRJ_RESPONSABILITY_DESC VARCHAR(255),
            PRJ_DWG_BASELINE_DT DATE,
            PRJ_DWG_BASELINE_DESC VARCHAR(255),
            PRJ_V_KEY_EVENT_IMPACTING_PROJECT_VALUE VARCHAR(255),
            PRJ_V_KEY_EVENT_POTENTIAL_IMPACT VARCHAR(255),
            PRJ_V_COMMITMENT_PIVOTAL VARCHAR(255),
            PRJ_V_PORTFOLIO_STRATEGIC_GROUPING VARCHAR(255),
            PRJ_BENCHMARK_MODALITY VARCHAR(255),
            PRJ_TPR_CATEGORY VARCHAR(255),
            PRJ_BLOCKBUSTER_OPPORTUNITY BOOLEAN,
            PRJ_PORTFOLIO_ID_VACCINES_PROJECTS VARCHAR(255),
            PRJ_8BY28 BOOLEAN,
            PRJ_TYPE VARCHAR(256),
            PRJ_SUB_TYPE VARCHAR(256),
            PRJ_SUB_ORG_TYPE VARCHAR(5000),
            PRJ_NEXT_MILESTONE_DATE DATE,
            PRJ_NEXT_MILESTONE_WBS_TYPE VARCHAR(4000),
            PRJ_TYPE_BUS_TERM VARCHAR(255),
            START_DT TIMESTAMP_NTZ(9),
            END_DT TIMESTAMP_NTZ(9),
            IS_LAST BOOLEAN,
            CREATED_BY VARCHAR(255),
            UPDATED_BY VARCHAR(255))
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table PROJECT successfully created")
                elif "already exists" in message:
                    print("PROJECT Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:
        result=cur.execute("""create table if not exists PROJECT_TYPE (
            TPR_ID NUMBER(28,0),
            TPR_CD VARCHAR(16777216),
            TPR_DESC VARCHAR(16777216),
            TPR_PRIME_TABLE VARCHAR(16777216),
            TPR_PRIME_CATEGORY VARCHAR(16777216),
            TPR_PRIME_PORTFOLIO VARCHAR(16777216),
            TPR_FIRST_CD VARCHAR(16777216),
            TPR_ORDER NUMBER(28,0),
            UPDATE_DT TIMESTAMP_NTZ(9),
            RW_UID VARCHAR(16777216),
            PROCESS_UID VARCHAR(16777216))
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table PROJECT_TYPE successfully created")
                elif "already exists" in message:
                    print("PROJECT_TYPE Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:
        result=cur.execute("""create table if not exists PRTFL_TCP_PROFILE (
            TCP_PROF_ID NUMBER(38,0) NOT NULL,
            TITLE VARCHAR(100),
            "ATTRIBUTE NAME" VARCHAR(100),
            INDICATION VARCHAR(200),
            "PROJECT CODE" VARCHAR(50),
            "PROJECT NAME" VARCHAR(200),
            COMMENTS VARCHAR(5000),
            STATUS VARCHAR(50),
            "CREATED BY" VARCHAR(50),
            "MODIFIED BY" VARCHAR(50),
            CREATED TIMESTAMP_NTZ(9),
            MODIFIED TIMESTAMP_NTZ(9)
        )COMMENT='This table contains TCP profile details in PRTFL_TCP_PROFILE, including project and indication'
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table PRTFL_TCP_PROFILE successfully created")
                elif "already exists" in message:
                    print("PRTFL_TCP_PROFILE Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:
        result=cur.execute("""create table if not exists PRTFL_TPP_PROFILE (
            TPP_PROF_ID NUMBER(38,0) NOT NULL,
            TITLE VARCHAR(250),
            "ATTRIBUTE NAME" VARCHAR(250),
            INDICATION VARCHAR(5000),
            "STANDARD OF CARE AT LAUNCH NAME" VARCHAR(250),
            "BASE PROFILE" VARCHAR(5000),
            "COMPARATIVE POSITION" VARCHAR(5000),
            "STANDARD OF CARE" VARCHAR(2048),
            "UPSIDE PROFILE" VARCHAR(5000),
            "MINIMALLY MARKETABLE PROFILE" VARCHAR(5000),
            "PROJECT CODE" VARCHAR(250),
            "PROJECT NAME" VARCHAR(250),
            "MINIMALLY VS SOC" VARCHAR(5000),
            "UPSIDE VS SOC" VARCHAR(250),
            STATUS VARCHAR(250),
            "CREATED BY" VARCHAR(250),
            "MODIFIED BY" VARCHAR(250),
            CREATED TIMESTAMP_NTZ(9),
            MODIFIED TIMESTAMP_NTZ(9),
            "SOC LAUNCH NAME 2" VARCHAR(250),
            "SOC DESCRIPTION 2" VARCHAR(5000),
            "COMPARATIVE POSITION 2" VARCHAR(250),
            "SOC COUNT" VARCHAR(250),
            "SOC LAUNCH NAME 3" VARCHAR(250),
            "SOC DESCRIPTION 3" VARCHAR(5000),
            "COMPARATIVE POSITION 3" VARCHAR(250),
            "UPSIDE VS SOC 2" VARCHAR(250),
            "UPSIDE VS SOC 3" VARCHAR(250),
            "MINIMALLY VS SOC 2" VARCHAR(250),
            "MINIMALLY VS SOC 3" VARCHAR(250),
            "SOC DESCRIPTION" VARCHAR(5000),
            "SOC LAUNCH NAME" VARCHAR(5000),
            PHASE1 VARCHAR(250),
            PHASE2 VARCHAR(250),
            PHASE3 VARCHAR(250),
            LATESTPUBLISHEDSOC VARCHAR(16777216),
            primary key (TPP_PROF_ID)
        )COMMENT='PORTFOLIO TPP PROFILE'
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table PRTFL_TPP_PROFILE successfully created")
                elif "already exists" in message:
                    print("PRTFL_TPP_PROFILE Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:
        result=cur.execute("""create table if not exists PRTFL_TVP_PROFILE (
            TVP_PROF_ID NUMBER(38,0) NOT NULL,
            TITLE VARCHAR(250),
            "ATTRIBUTE NAME" VARCHAR(250),
            INDICATION VARCHAR(250),
            "PROJECT CODE" VARCHAR(250),
            "PROJECT NAME" VARCHAR(250),
            COMMENTS VARCHAR(5000),
            STATUS VARCHAR(250),
            "CREATED BY" VARCHAR(250),
            "MODIFIED BY" VARCHAR(250),
            CREATED TIMESTAMP_NTZ(9),
            MODIFIED TIMESTAMP_NTZ(9),
            primary key (TVP_PROF_ID)
        )COMMENT='PORTFOLIO TVP PROFILE'
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table PRTFL_TVP_PROFILE successfully created")
                elif "already exists" in message:
                    print("PRTFL_TVP_PROFILE Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:
        result=cur.execute("""create table if not exists REF_BASELINE (
            TIME_ID VARCHAR(16777216),
            BAS_DESC VARCHAR(16777216),
            BAS_YEAR NUMBER(28,0),
            BAS_TYPE VARCHAR(16777216),
            BAS_PHARMA_FLAG BOOLEAN,
            BAS_VACCIN_FLAG BOOLEAN,
            BAS_ID NUMBER(28,0),
            BAS_PREV_BASELINE NUMBER(28,0),
            BAS_PREV_YEARLY NUMBER(28,0))
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table REF_BASELINE successfully created")
                elif "already exists" in message:
                    print("REF_BASELINE Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:
        result=cur.execute("""create table if not exists RESOURCE (
            TIME_ID VARCHAR(255),
            RES_ID VARCHAR(255),
            HUB_START_DT TIMESTAMP_NTZ(9),
            RES_PERC_ALLOCATION FLOAT,
            RES_PERC_CONTRACT FLOAT,
            RES_PERC_DIRECT FLOAT,
            RES_BASE_ENTITY VARCHAR(255),
            RES_BUILDING_NUM VARCHAR(255),
            RES_CALENDAR VARCHAR(255),
            RES_CONTRACT_TYPE VARCHAR(255),
            RES_COST_UNIT VARCHAR(255),
            RES_CONTRACT_END_DT DATE,
            RES_CONTRACT_START_DT DATE,
            RES_EMPLOYEE_NUM VARCHAR(255),
            RES_APPROACH_END_DT_FLAG BOOLEAN,
            RES_HEADCOUNT_EXCL_FLAG BOOLEAN,
            RES_INACTIVE_FLAG BOOLEAN,
            RES_MOVE_REASON VARCHAR(255),
            RES_NETWORK_ID VARCHAR(255),
            RES_OPEN_FLAG BOOLEAN,
            RES_OPERATIONALITY VARCHAR(255),
            RES_POSITION_NUM VARCHAR(255),
            RES_QUANTITY FLOAT,
            RES_RECRUITMENT_STATUS VARCHAR(255),
            RES_RECRUITMENT_TYPE VARCHAR(255),
            RES_RECRUITMENT_BKP VARCHAR(255),
            RES_MANAGER VARCHAR(255),
            RES_SKILL_TYPE VARCHAR(255),
            RES_SIMULATION_FLAG BOOLEAN,
            RES_PHYSICAL_SITE_FK VARCHAR(255),
            RES_MAIN_SKILL_FK VARCHAR(255),
            RES_TEAM VARCHAR(255),
            RES_TIMECARD_MANAGER VARCHAR(255),
            RES_TYPE_MOVE_IN VARCHAR(255),
            RES_TYPE_MOVE_OUT VARCHAR(255),
            RES_WORKDAY_NUM VARCHAR(255),
            RES_SERVICE_FOU_FK VARCHAR(255),
            RES_SHARED_FLAG BOOLEAN,
            RES_GREENLIGHT_DT DATE,
            RES_VACCIN_FLAG BOOLEAN,
            RES_PHARMA_FLAG BOOLEAN,
            RES_PERC_AVAILABILITY FLOAT,
            RES_ONB NUMBER(28,0),
            MD5 VARCHAR(255),
            CREATE_DT TIMESTAMP_NTZ(0),
            UPDATE_DT TIMESTAMP_NTZ(0),
            CREATED_BY VARCHAR(255),
            UPDATED_BY VARCHAR(255),
            RES_V_COST_CENTER VARCHAR(255),
            RES_V_DEPARTMENT_GROUP VARCHAR(255),
            RES_V_TODAY_AVAILABILITY NUMBER(28,0),
            RES_V_SKILLS VARCHAR(255),
            RES_V_EXCLUDE_ENTRY_FLAG BOOLEAN,
            RES_V_EXCLUDE_EXIT_FLAG BOOLEAN,
            RES_V_BUSINESS_UNIT_DESC VARCHAR(255),
            RES_V_DEPARTMENT_DESC VARCHAR(255),
            RES_V_PLATFORM_DESC VARCHAR(255),
            RES_V_TODAY_AVAIL_END_DT DATE,
            RES_COUNTRY VARCHAR(255),
            RES_CSU_REGION VARCHAR(255),
            RES_NM VARCHAR(255),
            RES_LAST_NM VARCHAR(255),
            RES_FIRST_NM VARCHAR(255),
            RES_DESC VARCHAR(255),
            RES_HIRING_MANAGER VARCHAR(255),
            RES_NAME_OF_THE_PERSON_REPLACED VARCHAR(255),
            RES_POSITION_ID VARCHAR(255),
            RES_MOVE_REASON_IN VARCHAR(255),
            RES_ONGOING_ABSENCE_REASON VARCHAR(255),
            RES_ABSENCE_START_DT DATE,
            RES_ABSENCE_END_DT DATE,
            RES_ABSENCE_ONGOING BOOLEAN,
            RES_V_EXTERNAL_FUNDING BOOLEAN,
            RES_V_CAPITALIZED BOOLEAN,
            RES_PROVIDER VARCHAR(255),
            RES_SKILL_LEVEL VARCHAR(255),
            RES_FUND_BY_NON_RD_DEPT BOOLEAN,
            RES_TSH_RESOURCE BOOLEAN,
            RES_USER_ACTIV_AD VARCHAR(255),
            RES_CSU_CLUSTER VARCHAR(4000),
            RES_COUNTRY_DESC VARCHAR(4000),
            RES_SHARED_FROM VARCHAR(255),
            RES_SHARED_TO VARCHAR(255),
            RES_SHARED_RBS_LINE_NUM NUMBER(16,2),
            START_DT TIMESTAMP_NTZ(9),
            END_DT TIMESTAMP_NTZ(9),
            IS_LAST BOOLEAN)
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table RESOURCE successfully created")
                elif "already exists" in message:
                    print("RESOURCE Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:
        result=cur.execute("""create table if not exists TASK (
            TIME_ID VARCHAR(255),
            TSK_WBS_ID VARCHAR(255),
            TSK_CD VARCHAR(255),
            HUB_START_DT TIMESTAMP_NTZ(0),
            TSK_PARENT_ROOT_TSK_WBS_ID VARCHAR(255),
            TSK_ACTUAL_FINISH_DT DATE,
            TSK_ACTUAL_START_DT DATE,
            TSK_ARMS_NUMBER NUMBER(28,0),
            TSK_CAMPAIGN_NUMBER VARCHAR(255),
            TSK_COMPLEXITY_FACTOR FLOAT,
            TSK_CRO_COST FLOAT,
            TSK_CYCLE VARCHAR(255),
            TSK_DS_DP_TO_PRODUCE VARCHAR(255),
            TSK_DURATION NUMBER(28,0),
            TSK_ALL_DURATIONS VARCHAR(255),
            TSK_END_DEFINITION VARCHAR(255),
            TSK_IP_BATCH VARCHAR(255),
            TSK_KITS_QTY NUMBER(28,0),
            TSK_KPI VARCHAR(255),
            TSK_KPI_DESC VARCHAR(255),
            TSK_LEADER VARCHAR(255),
            TSK_MANUFACTURING_PROCESS VARCHAR(255),
            TSK_MONITORING_SITE VARCHAR(255),
            TSK_NB_PLANNED_SITES FLOAT,
            TSK_NB_PLANNED_SITES_COHORT NUMBER(28,0),
            TSK_NB_PLANNED_SITES_FOLLOWUP NUMBER(28,0),
            TSK_NB_PLANNED_SUBJ FLOAT,
            TSK_NB_PLANNED_SUBJ_COHORT NUMBER(28,0),
            TSK_NB_PLANNED_SUBJ_FOLLOWUP FLOAT,
            TSK_NB_OF_ANALYTES NUMBER(28,0),
            TSK_OPERATIONAL_LEVEL_FLAG BOOLEAN,
            TSK_PACKAGING_TYPE VARCHAR(255),
            TSK_PLANNED_SAMPLES NUMBER(28,0),
            TSK_PLANNED_FINISH_DT DATE,
            TSK_PLANNED_START_DT DATE,
            TSK_PRODUCT_MANUFACT_LINE VARCHAR(255),
            TSK_PROJECT_LEVEL_FLAG BOOLEAN,
            TSK_PROTOCOL_SAMPLES NUMBER(28,0),
            TSK_PROVIDER VARCHAR(255),
            TSK_SAMPLE_COST FLOAT,
            TSK_SAMPLE_MGR_REF_TASK_FLAG BOOLEAN,
            TSK_SAMPLE_RATE NUMBER(28,0),
            TSK_SAMPLE_BY_SUBJECT FLOAT,
            TSK_SOURCING VARCHAR(255),
            TSK_START_DEFINITION VARCHAR(255),
            TSK_STORAGE_CONDITION VARCHAR(255),
            TSK_COUNTRY VARCHAR(255),
            TSK_REGION VARCHAR(255),
            TSK_PHARMA_FLAG BOOLEAN,
            TSK_VACCIN_FLAG BOOLEAN,
            TSK_CALENDAR_FLOAT FLOAT,
            TSK_CALENDAR_FREE_FLOAT NUMBER(28,0),
            TSK_PLW_IDENTIFIER VARCHAR(5000),
            TSK_NM VARCHAR(255),
            TSK_COMMENT VARCHAR(5000),
            TSK_ONB NUMBER(28,0),
            TSK_ACTIVITY_TYPE VARCHAR(255),
            TSK_PROJECT_MILESTONE_FLAG BOOLEAN,
            TSK_FIRST_TO_EXCLUDE_FLAG BOOLEAN,
            TSK_PROGRESS_COMPL_STATUS VARCHAR(255),
            TSK_TASK_RESPONSIBLE VARCHAR(255),
            TSK_PACK_ITEM_UNIT_COST NUMBER(28,0),
            TSK_PACK_TOTAL_UNIT_COST VARCHAR(255),
            TSK_END_OF_PHASE1 DATE,
            TSK_SITE VARCHAR(255),
            TSK_CSU_CLUSTER_DESC VARCHAR(255),
            TSK_END_RELEASE_DT DATE,
            TSK_TASK_TYPE VARCHAR(255),
            TSK_PACK_LOAD NUMBER(28,0),
            TSK_PACK_EXT_LOAD NUMBER(28,0),
            TSK_SPEC_TOOL VARCHAR(255),
            TSK_ORDER_NUMBER NUMBER(28,0),
            TSK_RELEASE_ACT_FINISH_DT DATE,
            TSK_V_BLOODDRAW_FLG BOOLEAN,
            TSK_V_CANCELLED VARCHAR(255),
            TSK_V_CRITICAL_FLG BOOLEAN,
            TSK_V_DEFINITION VARCHAR(5000),
            TSK_V_DELAY_ACTORS VARCHAR(255),
            TSK_V_DPT_GROUPING VARCHAR(255),
            TSK_V_DEVIATION_ROOT_CAUSE VARCHAR(255),
            TSK_V_DURATION_DEVIATION NUMBER(28,0),
            TSK_V_FUNC_WORKPACKAGE VARCHAR(255),
            TSK_V_GCI_RELEASE_DESC VARCHAR(255),
            TSK_V_GCI_RELEASE_NUM VARCHAR(255),
            TSK_V_KEY_MIL_FLG BOOLEAN,
            TSK_V_KEY_INFLEXION_POINT_FLG BOOLEAN,
            TSK_V_KEY_MIL_FUNC VARCHAR(255),
            TSK_V_KEY_MIL_NUM VARCHAR(255),
            TSK_V_KEY_MIL_PLATFORM VARCHAR(255),
            TSK_V_MIL_ACHIEVEMENT VARCHAR(255),
            TSK_V_MIL_PERIOD NUMBER(28,0),
            TSK_V_MIL_COMMENTS VARCHAR(255),
            TSK_V_GCI_NO_TESTING_FLG BOOLEAN,
            TSK_V_PROGRESS_DT DATE,
            TSK_V_ROOT_PRODUCT_CD VARCHAR(255),
            TSK_V_STEP_CD VARCHAR(255),
            TSK_V_STEP_DESC VARCHAR(255),
            TSK_V_STEP_NM VARCHAR(255),
            TSK_V_PRODUCT_REQUEST_FLG BOOLEAN,
            TSK_V_PROGRESS_STATUS VARCHAR(255),
            TSK_V_RISK_DELAY_FLG BOOLEAN,
            TSK_V_STEP_ONB NUMBER(28,0),
            TSK_REPORT_USED VARCHAR(255),
            TSK_V_IS_STEP_FLAG BOOLEAN,
            TSK_V_YEARLY_BASELINE_START_DT DATE,
            TSK_V_YEARLY_BASELINE_FINISH_DT DATE,
            TSK_V_RISK_DELAY_FLAG BOOLEAN,
            MD5 VARCHAR(255),
            CREATE_DT TIMESTAMP_NTZ(0),
            UPDATE_DT TIMESTAMP_NTZ(0),
            CREATED_BY VARCHAR(255),
            UPDATED_BY VARCHAR(255),
            TSK_CMC_KPI_FLAG BOOLEAN,
            TSK_SPECY VARCHAR(255),
            TSK_NB_ANIMALS NUMBER(28,0),
            TSK_V_VACCINATION_F_FLAG BOOLEAN,
            TSK_V_VACCINATION_FLAG BOOLEAN,
            TSK_V_CLI_PRJ_CAT VARCHAR(255),
            TSK_V_CLI_PRJ_SIZE VARCHAR(255),
            TSK_V_CLI_PRJ_COMPLEXITY VARCHAR(255),
            TSK_V_ONGOING_STUDY_COUNT NUMBER(28,0),
            TSK_V_STUDY_MANY_REGION NUMBER(28,0),
            TSK_V_CTDS_MAJOR_SUBMISSIONS NUMBER(28,0),
            TSK_V_GMP_PRODUCT VARCHAR(255),
            TSK_V_GMP_PRODUCT_PARENT VARCHAR(255),
            TSK_V_GMP_FILTERS_FLAG BOOLEAN,
            TSK_LVL VARCHAR(255),
            TSK_LINE_IDENTIFIER NUMBER(28,0),
            TSK_V_COMMITMENT_PIVOTAL VARCHAR(255),
            TSK_V_DEVELOPMENT_STRATEGY VARCHAR(255),
            TSK_V_AG_LIPID_DEPENDENT VARCHAR(255),
            TSK_V_EXTERNAL_PARTNER_WBS VARCHAR(255),
            TSK_V_KEY_MILESTONE_DEPARTMENT_CONTRIBUTORS VARCHAR(255),
            TSK_V_BUILDING_BLOCK_NM VARCHAR(255),
            TSK_V_BUILDING_BLOCK_IDENTIFY VARCHAR(255),
            TSK_V_BUILDING_BLOCK_STATUS VARCHAR(255),
            TSK_V_NBR_ANTIGEN NUMBER(28,0),
            TSK_V_NBR_COMMITMENT_PIVOTAL NUMBER(28,0),
            TSK_V_STUDY_CODE_CONSOLIDATION VARCHAR(255),
            TSK_V_GCI_INFORMATION_AVAILABLE BOOLEAN,
            TSK_V_GCI_ASSAY VARCHAR(255),
            TSK_V_GCI_LAB VARCHAR(255),
            TSK_V_GCI_SAMPLE_NUMBER NUMBER(28,0),
            TSK_V_RELEASE_NUMBER VARCHAR(255),
            TSK_V_GCI_ASSAY_PROVIDER VARCHAR(255),
            TSK_V_COUNTRY_AGENCY VARCHAR(255),
            TSK_V_ENDORSING_RATING VARCHAR(255),
            TSK_V_IS_FIRST BOOLEAN,
            TSK_V_IS_LAST BOOLEAN,
            TSK_VARIANCE_ANALYSIS VARCHAR(255),
            TSK_IS_A_TASK BOOLEAN,
            TSK_MILESTONE_CLINICAL_STUDY VARCHAR(255),
            TSK_ADJUVANT VARCHAR(255),
            TSK_MRNA_INITIATIVE_OBJECTIVE VARCHAR(255),
            TSK_ACT_COUNTRY_REG_F VARCHAR(255),
            TSK_NO_GCI_TESTING_TRIAL_STEP BOOLEAN,
            TSK_ENDORSED_RATING VARCHAR(255),
            TSK_PRIM_DOSE VARCHAR(255),
            YEARLY_BASELINE_FINISH_DATE_2014 DATE,
            YEARLY_BASELINE_START_DATE_2014 DATE,
            YEARLY_BASELINE_FINISH_DATE_2015 DATE,
            YEARLY_BASELINE_START_DATE_2015 DATE,
            YEARLY_BASELINE_FINISH_DATE_2016 DATE,
            YEARLY_BASELINE_START_DATE_2016 DATE,
            YEARLY_BASELINE_FINISH_DATE_2017 DATE,
            YEARLY_BASELINE_START_DATE_2017 DATE,
            YEARLY_BASELINE_START_DATE_2018 DATE,
            YEARLY_BASELINE_FINISH_DATE_2018 DATE,
            YEARLY_BASELINE_START_DATE_2019 DATE,
            YEARLY_BASELINE_FINISH_DATE_2019 DATE,
            YEARLY_BASELINE_START_DATE_2020 DATE,
            YEARLY_BASELINE_FINISH_DATE_2020 DATE,
            TSK_NEW_PRODUCTS_METRICS VARCHAR(255),
            TSK_V_FREQUENCY_SAMPLE_EXTRACTION NUMBER(28,0),
            TSK_V_COST_CENTER_ASSAYS_SAMPLE VARCHAR(255),
            TSK_V_GL_CODE_ASSAYS_SAMPLES VARCHAR(255),
            TSK_V_SAP_INTERNAL_ORDER VARCHAR(255),
            TSK_V_PO_NUMBER VARCHAR(255),
            TSK_V_PO_AMOUNT NUMBER(28,0),
            TSK_V_CASA_OR_NON_CASA VARCHAR(255),
            TSK_V_EXTERNAL_VENDOR_MANAGER_NAME VARCHAR(255),
            TSK_V_COST_CATEGORY_ASSAYS VARCHAR(255),
            TSK_V_REMAINING_AVAILABLE_PO_BALANCE NUMBER(28,0),
            TSK_V_PO_STATUS VARCHAR(255),
            TSK_V_TOTAL_GOOD_RECEIPTS NUMBER(28,0),
            TSK_V_MONTHLY_ACCRUAL_BASED_UPEN_EST_POC NUMBER(28,0),
            TSK_V_DELAY_CATEGORY VARCHAR(255),
            TSK_V_CSR_IN_CRITICAL_PATH BOOLEAN,
            TSK_V_DETAILED_DELAY VARCHAR(255),
            TSK_BUDGET_DECISION VARCHAR(4000),
            TSK_TSH_ACTIVITY VARCHAR(4000),
            TSK_PERCENTAGE_COMPLETE_ASSAY NUMBER(28,2),
            TSK_IS_TRANSVERSAL BOOLEAN,
            TSK_BATCH_FAILED BOOLEAN,
            TSK_BATCH_TYPE VARCHAR(255),
            TSK_BUILDING_BLOCK_DESCRIPTION VARCHAR(255),
            TSK_IS_A_PIVOTAL_ACTIVITY BOOLEAN,
            TSK_IS_A_COMMITMENT_ACTIVITY BOOLEAN,
            TSK_ON_CRITICAL_PATH BOOLEAN,
            TSK_PRP NUMBER(38,0),
            TSK_DS_DP_QTY_TO_BE_LAUNCHED VARCHAR(255),
            TSK_DS_DP_QTY_UNIT VARCHAR(255),
            TSK_PRODUCT_TYPE VARCHAR(255),
            TSK_DOSAGE_STRENGTH VARCHAR(255),
            TSK_DOSAGE_STRENGTH_UNIT VARCHAR(255),
            TSK_EARLIEST_MANUFACTURING_START_DATE DATE,
            TSK_LATEST_MANUFACTURING_END_DATE DATE,
            TSK_COMMITMENT_PIVOTAL_CALCULATED VARCHAR(255),
            TSK_LEADER_EMAIL VARCHAR(4000),
            TSK_MANUFACT_TYPE VARCHAR(4000),
            TSK_MSP_PREDECESSORS VARCHAR(4000),
            TSK_MSP_SUCCESSORS VARCHAR(4000),
            TSK_FVFS_LINKED_ASSAY DATE,
            TSK_LVLS_LINKED_ASSAY DATE,
            TSK_DBL_LINKED_REL_DATE DATE,
            TSK_STATE VARCHAR(255),
            TSK_BACK_UP_STRATEGY BOOLEAN,
            TSK_NEXT_READ_OUT BOOLEAN,
            TSK_PFM VARCHAR(4000),
            TSK_PFM_DESC VARCHAR(4000),
            TSK_PHARMA_FREE_FIELD_REP_1 VARCHAR(4000),
            TSK_PHARMA_FREE_FIELD_REP_2 VARCHAR(4000),
            TSK_V_MIL_TYPE VARCHAR(255),
            START_DT TIMESTAMP_NTZ(0),
            END_DT TIMESTAMP_NTZ(9),
            IS_LAST BOOLEAN)
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table TASK successfully created")
                elif "already exists" in message:
                    print("TASK Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:
        result=cur.execute("""create table if not exists TEAM_MEMBER (
            TIME_ID VARCHAR(255),
            IS_LAST BOOLEAN,
            WBS_ID VARCHAR(255),
            PTM_ID VARCHAR(255),
            PTM_PRJ_ROLE VARCHAR(255),
            PTM_PRJ_ROLE_DESC VARCHAR(255),
            PTM_SANOFI_ID VARCHAR(255),
            PTM_MEMBER_DESC VARCHAR(255),
            PTM_EMAIL VARCHAR(255),
            PTM_TEAMS VARCHAR(255),
            PTM_SUB_TEAMS VARCHAR(255),
            MD5 VARCHAR(255),
            START_DT TIMESTAMP_NTZ(9),
            CREATE_DT TIMESTAMP_NTZ(9),
            UPDATE_DT TIMESTAMP_NTZ(9),
            CREATED_BY VARCHAR(255),
            UPDATED_BY VARCHAR(255),
            END_DT TIMESTAMP_NTZ(9),
            PTM_DEPARTMENT VARCHAR(255),
            PTM_LOCATION VARCHAR(255),
            PTM_USER_INACTIVE BOOLEAN,
            PTM_BACK_UP VARCHAR(255),
            PTM_NOTE_PAD VARCHAR(255))
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table TEAM_MEMBER successfully created")
                elif "already exists" in message:
                    print("TEAM_MEMBER Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error
    try:
        result=cur.execute("""create table if not exists WBS_HIERARCHY (
            WBS_ID VARCHAR(255),
            WBS_TYPE VARCHAR(255),
            WBS_FUNCTIONAL_ID VARCHAR(255),
            PROJECT_ID VARCHAR(255),
            PRJ_FUNCTIONAL_ID VARCHAR(255),
            INDICATION_ID VARCHAR(16777216),
            IND_FUNCTIONAL_ID VARCHAR(16777216),
            PHASE_ID VARCHAR(16777216),
            PHA_FUNCTIONAL_ID VARCHAR(16777216),
            STUDY_ID VARCHAR(16777216),
            STU_FUNCTIONAL_ID VARCHAR(16777216),
            TASK_ID VARCHAR(16777216),
            TSK_FUNCTIONAL_ID NUMBER(28,0),
            TIME_ID VARCHAR(255),
            LV NUMBER(1,0),
            WBS_LIVE_FLAG BOOLEAN,
            WBS_PHARMA_FLAG BOOLEAN,
            WBS_VACCIN_FLAG BOOLEAN,
            WBS_TRANSVERSAL_FLAG BOOLEAN)
        """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("Table WBS_HIERARCHY successfully created")
                elif "already exists" in message:
                    print("WBS_HIERARCHY Table already exists, skipped creation")
    except Exception as e:
        print("Error:{e}")
        #Handle error    
def create_file_format():
    cur=_conn_adam()
    cur.execute("""use schema sales.landing""")
    print("\n//Creating file formats...")
    sql = """
    create file format if not exists ff_csv
    type = 'CSV'
    field_delimiter = ','
    skip_header = 1
    null_if = ('NULL', 'null')
    empty_field_as_null = true
    error_on_column_count_mismatch = false
    field_optionally_enclosed_by = '"'
    trim_space = true
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"file format 'ff_csv' created successfully")
            elif "already exists" in message:
                print(f"file format 'ff_csv' already exists, skipped creation")
    except Exception as e:
        print(f"Error creating file format 'ff_csv': {e}")
        
    sql = """
    create file format if not exists ff_parquet
    type = 'PARQUET'
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"file format 'ff_parquet' created successfully")
            elif "already exists" in message:
                print(f"file format 'ff_parquet' already exists, skipped creation")
    except Exception as e:
        print(f"Error creating file format 'ff_parquet': {e}")
        
    sql = """
    create file format if not exists ff_json
    type = 'JSON'
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"file format 'ff_json' created successfully")
            elif "already exists" in message:
                print(f"file format 'ff_json' already exists, skipped creation")
    except Exception as e:
        print(f"Error creating file format 'ff_json': {e}")
        
    cur.close()  
def create_local_stage():
    cur=_conn_adam()
    cur.execute("use schema sales.landing")
    print("\n//Creating local stages...")
    sql = f"""
    create stage if not exists local_csv_stage
    file_format = ff_csv
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"stage 'local_csv_stage' created successfully")
            elif "already exists" in message:
                print(f"stage 'local_csv_stage' already exists. Message, skipped creation")
    except Exception as e:
        print(f"Error creating stage 'local_csv_stage': {e}")

    sql = f"""
    create stage if not exists local_parquet_stage
    file_format = ff_parquet
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"stage 'local_parquet_stage' created successfully")
            elif "already exists" in message:
                print(f"stage 'local_parquet_stage' already exists. Message, skipped creation")
    except Exception as e:
        print(f"Error creating stage 'local_parquet_stage': {e}")
    
    sql = f"""
    create stage if not exists local_json_stage
    file_format = ff_json
    """
    try:
        result=cur.execute(sql)
        status=result.fetchone()
        if status:
            message=status[0]
            message=message.lower()
            if "successfully created" in message:
                print(f"stage 'local_json_stage' created successfully")
            elif "already exists" in message:
                print(f"stage 'local_json_stage' already exists. Message, skipped creation")
    except Exception as e:
        print(f"Error creating stage 'local_json_stage': {e}")      
def create_srv_rnd_df_views():
    cur=_conn_adam()    
    cur.execute("""use schema sales.srv_rnd_df""")
    print("\n-----------view Creation Starts-------------------")
    try: 
        result=cur.execute("""create view if not exists MVW_WBS_HIERARCHY(
	WBS_ID,
	WBS_TYPE,
	WBS_FUNCTIONAL_ID,
	PROJECT_ID,
	PRJ_FUNCTIONAL_ID,
	INDICATION_ID,
	IND_FUNCTIONAL_ID,
	PHASE_ID,
	PHA_FUNCTIONAL_ID,
	STUDY_ID,
	STU_FUNCTIONAL_ID,
	TASK_ID,
	TSK_FUNCTIONAL_ID,
	TIME_ID,
	LV,
	WBS_LIVE_FLAG,
	WBS_PHARMA_FLAG,
	WBS_VACCIN_FLAG,
	WBS_TRANSVERSAL_FLAG
) as select * from LANDING.WBS_HIERARCHY
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view MVW_WBS_HIERARCHY successfully created")
                elif "already exists" in message:
                    print("MVW_WBS_HIERARCHY view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view MVW_WBS_HIERARCHY: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists VW_INDICATION(
	TIME_ID,
	IND_WBS_ID,
	IND_UNIQUE_CD,
	HUB_START_DT,
	IND_POS_TO_POCC,
	IND_POTS,
	IND_SR_POCC,
	IND_NEXT_PHASE_SUCCESS_RATE,
	IND_NEXT_PHASE_PRP,
	IND_DEV_OBJECTIVE,
	IND_FORMULATION,
	IND_NUMBER,
	IND_PHASE,
	IND_PRIORITY,
	IND_STATUS,
	IND_STATUS_DETAILED,
	IND_THP_FK,
	IND_CD,
	IND_ACTUAL_START_DT,
	IND_PLANNED_START_DT,
	IND_ACTUAL_FINISH_DT,
	IND_PLANNED_FINISH_DT,
	IND_ADMIN_ROUTE,
	IND_FOU_FK,
	IND_DESC,
	IND_PHARMA_FLAG,
	IND_VACCIN_FLAG,
	IND_LEAD_FLAG,
	IND_NEXT_GNG_DT,
	IND_NEXT_PHASE,
	IND_NEXT_PHASE_START_DT,
	IND_STOPPED_DT,
	MD5,
	CREATE_TS,
	UPDATE_TS,
	CREATED_BY,
	UPDATED_BY,
	IND_ONB,
	IND_V_COST_LAUNCH,
	IND_V_CUSTO_PRJ_FLAG,
	IND_V_INC_YEAR_CUMUL,
	IND_V_PEAK_SALES,
	IND_V_IND_DRIVER,
	IND_V_IND_OBJ,
	IND_V_NPV,
	IND_V_PRIO_COMMENT,
	IND_V_REASON_STOP,
	IND_V_EXP_SYSTEM,
	IND_V_SC_SHORT_NAME,
	IND_V_SC_ASSUMPTION,
	IND_V_MAIN_CHANGES,
	IND_V_MARKET_POSITION,
	IND_V_MARKET_RATIONAL,
	IND_V_BUS_SUSTAINABILITY_FLAG,
	IND_V_COMMITMENT,
	IND_V_COMM_OPPORTUNITY,
	IND_V_VELOCITY,
	IND_SHORTNAME,
	IND_V_PRIORITY,
	IND_V_SITE,
	IND_V_FINANCIAL_CATEGORY,
	IND_V_PRODUCT_CD_SYNONYM,
	IND_V_ALL_ROOT_PRODUCT_CODES,
	IND_REPORTING,
	IND_BENCHMARK_FORMULATION,
	IND_V_PORTFOLIO_STRATEGIC_GROUPING,
	IND_V_COMMITMENT_PIVOTAL,
	IND_V_NBR_ANTIGEN,
	IND_V_NBR_COMMITMENT_PIVOTAL,
	IND_TERMINATION_REASON,
	IND_FREE_FIELD_PROJECT_PPR,
	IND_PFM,
	IND_PFM_DESC,
	IND_ECODES,
	IND_ECODESIGN_STATUS,
	IND_CLIMATE_CHANGE_IMPACT,
	START_DT,
	END_DT,
	IS_LAST
) as select * from landing.indication
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_INDICATION successfully created")
                elif "already exists" in message:
                    print("VW_INDICATION view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_INDICATION: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists VW_PHASE(
	TIME_ID,
	PHA_WBS_ID,
	PHA_UNIQUE_CD,
	HUB_START_DT,
	PHA_SUCCESS_RATE,
	PHA_PRP,
	PHA_CD,
	PHA_WEIGHTING,
	PHA_PLANNED_START_DT,
	PHA_PLANNED_FINISH_DT,
	PHA_ACTUAL_START_DT,
	PHA_ACTUAL_FINISH_DT,
	PHA_ONB,
	PHA_ORDER_NM,
	PHA_DESC,
	PHA_CURRENT_PHASE_FLAG,
	PHA_PHARMA_FLAG,
	PHA_VACCIN_FLAG,
	PHA_V_REPORT_PHASE_FLG,
	PHA_V_SUCCES_RATE,
	PHA_V_SUCCES_RATE_APPROVAL_DT,
	PHA_V_TYPE,
	MD5,
	CREATE_DT,
	UPDATE_DT,
	CREATED_BY,
	UPDATED_BY,
	PHA_V_YEARLY_START_DT,
	PHA_V_YEARLY_FINISH_DT,
	PHA_BUDGETED,
	YEARLY_BASELINE_FINISH_DATE_2014,
	YEARLY_BASELINE_START_DATE_2014,
	YEARLY_BASELINE_FINISH_DATE_2015,
	YEARLY_BASELINE_START_DATE_2015,
	YEARLY_BASELINE_FINISH_DATE_2016,
	YEARLY_BASELINE_START_DATE_2016,
	YEARLY_BASELINE_FINISH_DATE_2017,
	YEARLY_BASELINE_START_DATE_2017,
	YEARLY_BASELINE_START_DATE_2018,
	YEARLY_BASELINE_FINISH_DATE_2018,
	YEARLY_BASELINE_START_DATE_2019,
	YEARLY_BASELINE_FINISH_DATE_2019,
	YEARLY_BASELINE_START_DATE_2020,
	YEARLY_BASELINE_FINISH_DATE_2020,
	START_DT,
	END_DT,
	IS_LAST
) as select * from landing.phase
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PHASE successfully created")
                elif "already exists" in message:
                    print("VW_PHASE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PHASE: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists VW_PROJECT(
	TIME_ID,
	PRJ_WBS_ID,
	PRJ_CD,
	HUB_START_DT,
	PRJ_ONB,
	PRJ_NM,
	PRJ_DESC,
	PRJ_COM_TERMINATION,
	PRJ_TERMINATION_REASON,
	PRJ_ADMINISTRATION_ROUTE,
	PRJ_ANTIGEN,
	PRJ_BRAND_NM,
	PRJ_CMC_PORTFOLIO,
	PRJ_CODEV_PARTNER,
	PRJ_PIPELINE_COMMENT,
	PRJ_CREATION_DT,
	PRJ_CUSTOMIZED_FLAG,
	PRJ_COST_LAUNCH_RELATED_DT,
	PRJ_ACQUISITION_DT,
	PRJ_COMPLETION_DT,
	PRJ_TERMINATION_DT,
	PRJ_DEV_DEVICE_FLAG,
	PRJ_DISCO_DEV_LINKED_CODES,
	PRJ_ENTERING_PREDEV_DT,
	PRJ_ENTERING_DEV_DT,
	PRJ_EXITING_DEV_DT,
	PRJ_EXITING_PREDEV_DT,
	PRJ_EXP_GENERIC_ENTRY_DT,
	PRJ_FRANCHISE,
	PRJ_FUNDING_ZONE,
	PRJ_GEOGRAPHICAL_TARGET,
	PRJ_HUB_OWNER,
	PRJ_INN,
	PRJ_INNOVATION_STATUS,
	PRJ_MOA,
	PRJ_MOLECULE_SUBTYPE,
	PRJ_MOLECULE_TYPE,
	PRJ_OBJECTIVE,
	PRJ_PARTNER_NM,
	PRJ_NME_ORIGIN,
	PRJ_OWNER,
	PRJ_PATENT_INFORMATION,
	PRJ_PATHOGEN,
	PRJ_V_PPP_PRJ_LEADER,
	PRJ_V_PPP_PRJ_MANAGER,
	PRJ_PLANNED_FINISH_DT,
	PRJ_PLANNED_START_DT,
	PRJ_TPR_FK,
	PRJ_PROJECT_LEADER_ENTRY,
	PRJ_PHASE,
	PRJ_EBINDER_LINK,
	PRJ_SITE,
	PRJ_STATUS,
	PRJ_STATUS_DETAILED,
	PRJ_SUBCATEGORY,
	PRJ_RESPONSABILITY_FOU_FK,
	PRJ_ROOT_PRODUCT,
	PRJ_PUBLIC_FUNDING_ORG,
	PRJ_RECOMMANNDATION,
	PRJ_STAGE,
	PRJ_VACCIN_CATEGORY,
	PRJ_STATE,
	PRJ_VACCIN_TYPE,
	PRJ_VARIANCE_ANALYSIS,
	PRJ_APPROACH_PHASE_AT_PRIO,
	PRJ_PROJECT_MANAGER,
	PRJ_PARTNER_PRODUCT_CD,
	PRJ_CLUSTER_CD,
	PRJ_CLUSTER_DESC,
	PRJ_PORTFOLIO_MAIN,
	PRJ_PORTFOLIO,
	PRJ_DATABASE,
	PRJ_PHARMA_FLAG,
	PRJ_VACCIN_FLAG,
	PRJ_PRIORITY,
	PRJ_DEV_ENTRY_DT,
	PRJ_FIRST_APPROACH_DT,
	PRJ_NEXT_GNG_DT,
	PRJ_NEXT_GNG_CD,
	PRJ_PERM_PROJECT_FLAG,
	PRJ_NAME_EXT_SOURCE,
	PRJ_V_GLOBAL_PRJ_HEAD,
	PRJ_V_TARGET_POPULATION,
	PRJ_V_SHINE_PRJ_CD,
	PRJ_V_PRIORITY,
	PRJ_MOLECULE_TYPE_CD,
	PRJ_MOLECULE_SUBTYPE_CD,
	PRJ_V_APAO_PRJ_LIST,
	PRJ_V_APAO_PRJ_FLAG,
	PRJ_V_KHM,
	PRJ_MOA_SHORT_NM,
	MD5,
	CREATE_TS,
	UPDTED_TS,
	PRJ_V_FINANCIAL_CATEGORY,
	PRJ_PHARMACOLOGICAL_EFFECT,
	PRJ_CYCLE,
	PRJ_V_PRODUCT_CD_SYNONYM,
	PRJ_V_ALL_PRODUCT_CODES,
	PRJ_REPORTING,
	PRJ_RESPONSABILITY_DESC,
	PRJ_DWG_BASELINE_DT,
	PRJ_DWG_BASELINE_DESC,
	PRJ_V_KEY_EVENT_IMPACTING_PROJECT_VALUE,
	PRJ_V_KEY_EVENT_POTENTIAL_IMPACT,
	PRJ_V_COMMITMENT_PIVOTAL,
	PRJ_V_PORTFOLIO_STRATEGIC_GROUPING,
	PRJ_BENCHMARK_MODALITY,
	PRJ_TPR_CATEGORY,
	PRJ_BLOCKBUSTER_OPPORTUNITY,
	PRJ_PORTFOLIO_ID_VACCINES_PROJECTS,
	PRJ_8BY28,
	PRJ_TYPE,
	PRJ_SUB_TYPE,
	PRJ_SUB_ORG_TYPE,
	PRJ_NEXT_MILESTONE_DATE,
	PRJ_NEXT_MILESTONE_WBS_TYPE,
	PRJ_TYPE_BUS_TERM,
	START_DT,
	END_DT,
	IS_LAST,
	CREATED_BY,
	UPDATED_BY
) as select * from landing.project
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT: {e}")
        #Handle error

    try: 
        result=cur.execute("""create view if not exists VW_REF_BASELINE(
	TIME_ID,
	BAS_DESC,
	BAS_YEAR,
	BAS_TYPE,
	BAS_PHARMA_FLAG,
	BAS_VACCIN_FLAG,
	BAS_ID,
	BAS_PREV_BASELINE,
	BAS_PREV_YEARLY
) as select * from landing.ref_baseline
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_REF_BASELINE successfully created")
                elif "already exists" in message:
                    print("VW_REF_BASELINE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_REF_BASELINE: {e}")
        #Handle error

    try: 
        result=cur.execute("""create view if not exists VW_RESOURCE(
	TIME_ID,
	RES_ID,
	HUB_START_DT,
	RES_PERC_ALLOCATION,
	RES_PERC_CONTRACT,
	RES_PERC_DIRECT,
	RES_BASE_ENTITY,
	RES_BUILDING_NUM,
	RES_CALENDAR,
	RES_CONTRACT_TYPE,
	RES_COST_UNIT,
	RES_CONTRACT_END_DT,
	RES_CONTRACT_START_DT,
	RES_EMPLOYEE_NUM,
	RES_APPROACH_END_DT_FLAG,
	RES_HEADCOUNT_EXCL_FLAG,
	RES_INACTIVE_FLAG,
	RES_MOVE_REASON,
	RES_NETWORK_ID,
	RES_OPEN_FLAG,
	RES_OPERATIONALITY,
	RES_POSITION_NUM,
	RES_QUANTITY,
	RES_RECRUITMENT_STATUS,
	RES_RECRUITMENT_TYPE,
	RES_RECRUITMENT_BKP,
	RES_MANAGER,
	RES_SKILL_TYPE,
	RES_SIMULATION_FLAG,
	RES_PHYSICAL_SITE_FK,
	RES_MAIN_SKILL_FK,
	RES_TEAM,
	RES_TIMECARD_MANAGER,
	RES_TYPE_MOVE_IN,
	RES_TYPE_MOVE_OUT,
	RES_WORKDAY_NUM,
	RES_SERVICE_FOU_FK,
	RES_SHARED_FLAG,
	RES_GREENLIGHT_DT,
	RES_VACCIN_FLAG,
	RES_PHARMA_FLAG,
	RES_PERC_AVAILABILITY,
	RES_ONB,
	MD5,
	CREATE_DT,
	UPDATE_DT,
	CREATED_BY,
	UPDATED_BY,
	RES_V_COST_CENTER,
	RES_V_DEPARTMENT_GROUP,
	RES_V_TODAY_AVAILABILITY,
	RES_V_SKILLS,
	RES_V_EXCLUDE_ENTRY_FLAG,
	RES_V_EXCLUDE_EXIT_FLAG,
	RES_V_BUSINESS_UNIT_DESC,
	RES_V_DEPARTMENT_DESC,
	RES_V_PLATFORM_DESC,
	RES_V_TODAY_AVAIL_END_DT,
	RES_COUNTRY,
	RES_CSU_REGION,
	RES_NM,
	RES_LAST_NM,
	RES_FIRST_NM,
	RES_DESC,
	RES_HIRING_MANAGER,
	RES_NAME_OF_THE_PERSON_REPLACED,
	RES_POSITION_ID,
	RES_MOVE_REASON_IN,
	RES_ONGOING_ABSENCE_REASON,
	RES_ABSENCE_START_DT,
	RES_ABSENCE_END_DT,
	RES_ABSENCE_ONGOING,
	RES_V_EXTERNAL_FUNDING,
	RES_V_CAPITALIZED,
	RES_PROVIDER,
	RES_SKILL_LEVEL,
	RES_FUND_BY_NON_RD_DEPT,
	RES_TSH_RESOURCE,
	RES_USER_ACTIV_AD,
	RES_CSU_CLUSTER,
	RES_COUNTRY_DESC,
	RES_SHARED_FROM,
	RES_SHARED_TO,
	RES_SHARED_RBS_LINE_NUM,
	START_DT,
	END_DT,
	IS_LAST
) as select * from landing.resource
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_RESOURCE successfully created")
                elif "already exists" in message:
                    print("VW_RESOURCE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_RESOURCE: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists VW_TASK(
	TIME_ID,
	TSK_WBS_ID,
	TSK_CD,
	HUB_START_DT,
	TSK_PARENT_ROOT_TSK_WBS_ID,
	TSK_ACTUAL_FINISH_DT,
	TSK_ACTUAL_START_DT,
	TSK_ARMS_NUMBER,
	TSK_CAMPAIGN_NUMBER,
	TSK_COMPLEXITY_FACTOR,
	TSK_CRO_COST,
	TSK_CYCLE,
	TSK_DS_DP_TO_PRODUCE,
	TSK_DURATION,
	TSK_ALL_DURATIONS,
	TSK_END_DEFINITION,
	TSK_IP_BATCH,
	TSK_KITS_QTY,
	TSK_KPI,
	TSK_KPI_DESC,
	TSK_LEADER,
	TSK_MANUFACTURING_PROCESS,
	TSK_MONITORING_SITE,
	TSK_NB_PLANNED_SITES,
	TSK_NB_PLANNED_SITES_COHORT,
	TSK_NB_PLANNED_SITES_FOLLOWUP,
	TSK_NB_PLANNED_SUBJ,
	TSK_NB_PLANNED_SUBJ_COHORT,
	TSK_NB_PLANNED_SUBJ_FOLLOWUP,
	TSK_NB_OF_ANALYTES,
	TSK_OPERATIONAL_LEVEL_FLAG,
	TSK_PACKAGING_TYPE,
	TSK_PLANNED_SAMPLES,
	TSK_PLANNED_FINISH_DT,
	TSK_PLANNED_START_DT,
	TSK_PRODUCT_MANUFACT_LINE,
	TSK_PROJECT_LEVEL_FLAG,
	TSK_PROTOCOL_SAMPLES,
	TSK_PROVIDER,
	TSK_SAMPLE_COST,
	TSK_SAMPLE_MGR_REF_TASK_FLAG,
	TSK_SAMPLE_RATE,
	TSK_SAMPLE_BY_SUBJECT,
	TSK_SOURCING,
	TSK_START_DEFINITION,
	TSK_STORAGE_CONDITION,
	TSK_COUNTRY,
	TSK_REGION,
	TSK_PHARMA_FLAG,
	TSK_VACCIN_FLAG,
	TSK_CALENDAR_FLOAT,
	TSK_CALENDAR_FREE_FLOAT,
	TSK_PLW_IDENTIFIER,
	TSK_NM,
	TSK_COMMENT,
	TSK_ONB,
	TSK_ACTIVITY_TYPE,
	TSK_PROJECT_MILESTONE_FLAG,
	TSK_FIRST_TO_EXCLUDE_FLAG,
	TSK_PROGRESS_COMPL_STATUS,
	TSK_TASK_RESPONSIBLE,
	TSK_PACK_ITEM_UNIT_COST,
	TSK_PACK_TOTAL_UNIT_COST,
	TSK_END_OF_PHASE1,
	TSK_SITE,
	TSK_CSU_CLUSTER_DESC,
	TSK_END_RELEASE_DT,
	TSK_TASK_TYPE,
	TSK_PACK_LOAD,
	TSK_PACK_EXT_LOAD,
	TSK_SPEC_TOOL,
	TSK_ORDER_NUMBER,
	TSK_RELEASE_ACT_FINISH_DT,
	TSK_V_BLOODDRAW_FLG,
	TSK_V_CANCELLED,
	TSK_V_CRITICAL_FLG,
	TSK_V_DEFINITION,
	TSK_V_DELAY_ACTORS,
	TSK_V_DPT_GROUPING,
	TSK_V_DEVIATION_ROOT_CAUSE,
	TSK_V_DURATION_DEVIATION,
	TSK_V_FUNC_WORKPACKAGE,
	TSK_V_GCI_RELEASE_DESC,
	TSK_V_GCI_RELEASE_NUM,
	TSK_V_KEY_MIL_FLG,
	TSK_V_KEY_INFLEXION_POINT_FLG,
	TSK_V_KEY_MIL_FUNC,
	TSK_V_KEY_MIL_NUM,
	TSK_V_KEY_MIL_PLATFORM,
	TSK_V_MIL_ACHIEVEMENT,
	TSK_V_MIL_PERIOD,
	TSK_V_MIL_COMMENTS,
	TSK_V_GCI_NO_TESTING_FLG,
	TSK_V_PROGRESS_DT,
	TSK_V_ROOT_PRODUCT_CD,
	TSK_V_STEP_CD,
	TSK_V_STEP_DESC,
	TSK_V_STEP_NM,
	TSK_V_PRODUCT_REQUEST_FLG,
	TSK_V_PROGRESS_STATUS,
	TSK_V_RISK_DELAY_FLG,
	TSK_V_STEP_ONB,
	TSK_REPORT_USED,
	TSK_V_IS_STEP_FLAG,
	TSK_V_YEARLY_BASELINE_START_DT,
	TSK_V_YEARLY_BASELINE_FINISH_DT,
	TSK_V_RISK_DELAY_FLAG,
	MD5,
	CREATE_DT,
	UPDATE_DT,
	CREATED_BY,
	UPDATED_BY,
	TSK_CMC_KPI_FLAG,
	TSK_SPECY,
	TSK_NB_ANIMALS,
	TSK_V_VACCINATION_F_FLAG,
	TSK_V_VACCINATION_FLAG,
	TSK_V_CLI_PRJ_CAT,
	TSK_V_CLI_PRJ_SIZE,
	TSK_V_CLI_PRJ_COMPLEXITY,
	TSK_V_ONGOING_STUDY_COUNT,
	TSK_V_STUDY_MANY_REGION,
	TSK_V_CTDS_MAJOR_SUBMISSIONS,
	TSK_V_GMP_PRODUCT,
	TSK_V_GMP_PRODUCT_PARENT,
	TSK_V_GMP_FILTERS_FLAG,
	TSK_LVL,
	TSK_LINE_IDENTIFIER,
	TSK_V_COMMITMENT_PIVOTAL,
	TSK_V_DEVELOPMENT_STRATEGY,
	TSK_V_AG_LIPID_DEPENDENT,
	TSK_V_EXTERNAL_PARTNER_WBS,
	TSK_V_KEY_MILESTONE_DEPARTMENT_CONTRIBUTORS,
	TSK_V_BUILDING_BLOCK_NM,
	TSK_V_BUILDING_BLOCK_IDENTIFY,
	TSK_V_BUILDING_BLOCK_STATUS,
	TSK_V_NBR_ANTIGEN,
	TSK_V_NBR_COMMITMENT_PIVOTAL,
	TSK_V_STUDY_CODE_CONSOLIDATION,
	TSK_V_GCI_INFORMATION_AVAILABLE,
	TSK_V_GCI_ASSAY,
	TSK_V_GCI_LAB,
	TSK_V_GCI_SAMPLE_NUMBER,
	TSK_V_RELEASE_NUMBER,
	TSK_V_GCI_ASSAY_PROVIDER,
	TSK_V_COUNTRY_AGENCY,
	TSK_V_ENDORSING_RATING,
	TSK_V_IS_FIRST,
	TSK_V_IS_LAST,
	TSK_VARIANCE_ANALYSIS,
	TSK_IS_A_TASK,
	TSK_MILESTONE_CLINICAL_STUDY,
	TSK_ADJUVANT,
	TSK_MRNA_INITIATIVE_OBJECTIVE,
	TSK_ACT_COUNTRY_REG_F,
	TSK_NO_GCI_TESTING_TRIAL_STEP,
	TSK_ENDORSED_RATING,
	TSK_PRIM_DOSE,
	YEARLY_BASELINE_FINISH_DATE_2014,
	YEARLY_BASELINE_START_DATE_2014,
	YEARLY_BASELINE_FINISH_DATE_2015,
	YEARLY_BASELINE_START_DATE_2015,
	YEARLY_BASELINE_FINISH_DATE_2016,
	YEARLY_BASELINE_START_DATE_2016,
	YEARLY_BASELINE_FINISH_DATE_2017,
	YEARLY_BASELINE_START_DATE_2017,
	YEARLY_BASELINE_START_DATE_2018,
	YEARLY_BASELINE_FINISH_DATE_2018,
	YEARLY_BASELINE_START_DATE_2019,
	YEARLY_BASELINE_FINISH_DATE_2019,
	YEARLY_BASELINE_START_DATE_2020,
	YEARLY_BASELINE_FINISH_DATE_2020,
	TSK_NEW_PRODUCTS_METRICS,
	TSK_V_FREQUENCY_SAMPLE_EXTRACTION,
	TSK_V_COST_CENTER_ASSAYS_SAMPLE,
	TSK_V_GL_CODE_ASSAYS_SAMPLES,
	TSK_V_SAP_INTERNAL_ORDER,
	TSK_V_PO_NUMBER,
	TSK_V_PO_AMOUNT,
	TSK_V_CASA_OR_NON_CASA,
	TSK_V_EXTERNAL_VENDOR_MANAGER_NAME,
	TSK_V_COST_CATEGORY_ASSAYS,
	TSK_V_REMAINING_AVAILABLE_PO_BALANCE,
	TSK_V_PO_STATUS,
	TSK_V_TOTAL_GOOD_RECEIPTS,
	TSK_V_MONTHLY_ACCRUAL_BASED_UPEN_EST_POC,
	TSK_V_DELAY_CATEGORY,
	TSK_V_CSR_IN_CRITICAL_PATH,
	TSK_V_DETAILED_DELAY,
	TSK_BUDGET_DECISION,
	TSK_TSH_ACTIVITY,
	TSK_PERCENTAGE_COMPLETE_ASSAY,
	TSK_IS_TRANSVERSAL,
	TSK_BATCH_FAILED,
	TSK_BATCH_TYPE,
	TSK_BUILDING_BLOCK_DESCRIPTION,
	TSK_IS_A_PIVOTAL_ACTIVITY,
	TSK_IS_A_COMMITMENT_ACTIVITY,
	TSK_ON_CRITICAL_PATH,
	TSK_PRP,
	TSK_DS_DP_QTY_TO_BE_LAUNCHED,
	TSK_DS_DP_QTY_UNIT,
	TSK_PRODUCT_TYPE,
	TSK_DOSAGE_STRENGTH,
	TSK_DOSAGE_STRENGTH_UNIT,
	TSK_EARLIEST_MANUFACTURING_START_DATE,
	TSK_LATEST_MANUFACTURING_END_DATE,
	TSK_COMMITMENT_PIVOTAL_CALCULATED,
	TSK_LEADER_EMAIL,
	TSK_MANUFACT_TYPE,
	TSK_MSP_PREDECESSORS,
	TSK_MSP_SUCCESSORS,
	TSK_FVFS_LINKED_ASSAY,
	TSK_LVLS_LINKED_ASSAY,
	TSK_DBL_LINKED_REL_DATE,
	TSK_STATE,
	TSK_BACK_UP_STRATEGY,
	TSK_NEXT_READ_OUT,
	TSK_PFM,
	TSK_PFM_DESC,
	TSK_PHARMA_FREE_FIELD_REP_1,
	TSK_PHARMA_FREE_FIELD_REP_2,
	TSK_V_MIL_TYPE,
	START_DT,
	END_DT,
	IS_LAST
) as select * from landing.task
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_TASK successfully created")
                elif "already exists" in message:
                    print("VW_TASK view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_TASK: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists VW_TEAM_MEMBER(
	TIME_ID,
	IS_LAST,
	WBS_ID,
	PTM_ID,
	PTM_PRJ_ROLE,
	PTM_PRJ_ROLE_DESC,
	PTM_SANOFI_ID,
	PTM_MEMBER_DESC,
	PTM_EMAIL,
	PTM_TEAMS,
	PTM_SUB_TEAMS,
	MD5,
	START_DT,
	CREATE_DT,
	UPDATE_DT,
	CREATED_BY,
	UPDATED_BY,
	END_DT,
	PTM_DEPARTMENT,
	PTM_LOCATION,
	PTM_USER_INACTIVE,
	PTM_BACK_UP,
	PTM_NOTE_PAD
) as select * from landing.team_member
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_TEAM_MEMBER successfully created")
                elif "already exists" in message:
                    print("VW_TEAM_MEMBER view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_TEAM_MEMBER: {e}")
        #Handle error   
def create_srv_mdm_rndmasterdata_views():
    cur=_conn_adam()    
    cur.execute("""use schema sales.srv_mdm_rndmasterdata""")
    print("\n-----------view Creation Starts for schema srv_mdm_rndmasterdata-------------------")
    try: 
        result=cur.execute("""create view if not exists VW_MDM_CLINICAL_INDICATION(
	RDM_NAME_NM,
	RDM_CODE_CD,
	MEDDRA_TERM,
	ACRONYM,
	ISACTIVE,
	CREATED_BY,
	CREATE_DATE_TS,
	UPDATED_BY,
	LAST_UPDATE_DATE_TS,
	SOURCE_SYSTEM
) as select * from landing.mdm_clinical_indication
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MDM_CLINICAL_INDICATION successfully created")
                elif "already exists" in message:
                    print("VW_MDM_CLINICAL_INDICATION view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MDM_CLINICAL_INDICATION: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists VW_MDM_FINANCIAL_ORGANIZATION_UNIT(
	RDM_CODE_CD,
	RDM_NAME_NM,
	TYPE,
	EN_NM,
	PARENT_CODE_CD,
	LEVEL2TYPE,
	ISACTIVE,
	CREATED_BY,
	CREATE_DATE_TS,
	UPDATED_BY,
	LAST_UPDATE_DATE_TS,
	SOURCE_SYSTEM
) as select * from landing.mdm_financial_organization_unit
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MDM_FINANCIAL_ORGANIZATION_UNIT successfully created")
                elif "already exists" in message:
                    print("VW_MDM_FINANCIAL_ORGANIZATION_UNIT view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MDM_FINANCIAL_ORGANIZATION_UNIT: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists VW_MDM_PROJECT_IND_MASTER(
	ID,
	SOURCE_PKEY,
	BUSINESS_ID,
	PROJECT_IND_CODE_CD,
	PROJECT_IND_NAME_NM,
	PROJECT_IND_DESCRIPTION_DESC,
	PROJECT_IND_RESPONSIBLE,
	PROJECT_IND_STATUS,
	PROJECT_IND_STATUS_DETAILED,
	CLINICAL_IND,
	MEDICAL_THERAPEUTIC_AREA,
	SOURCE_SYSTEM,
	CREATIONDATE_DT,
	LASTUPDATEDATE_DT,
	CREATEDBY,
	UPDATEDBY,
	PROJECT_IND_PHASE,
	STATE
) as select * from landing.mdm_project_ind_master
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MDM_PROJECT_IND_MASTER successfully created")
                elif "already exists" in message:
                    print("VW_MDM_PROJECT_IND_MASTER view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MDM_PROJECT_IND_MASTER: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists VW_MDM_PROJECT_MASTER(
	ID,
	SOURCE_PKEY,
	BUSINESS_ID,
	PROJECT_CODE_CD,
	PROJECT_RESPONSIBLE,
	PROJECT_ORGANIZATION_TYPE,
	PROJECT_TYPE,
	PROJECT_SUBTYPE,
	PROJECT_NAME_NM,
	PROJECT_DESCRIPTION_DESC,
	PROJECT_CATEGORY,
	PROJECT_STATUS,
	PROJECT_STATUS_DETAILED,
	PROJECT_PHASE,
	MECHANISM_OF_ACTION,
	ACTIVE_SUBSTANCE_TYPE,
	ACTIVE_SUBSTANCE_SUB_TYPE,
	ORIGIN_OF_ACTIVE_SUBSTANCE,
	ORIGIN_COMPANY_OF_ACTIVE_SUBSTANCE,
	EXTERNAL_ACTIVE_SUBSTANCE_CODE,
	DATE_OF_AGREEMENT,
	BRAND_NAME_NM,
	INN,
	RA_CODE,
	ADDITIONAL_PROJECT_INFORMATION,
	RESEARCH_PROJECT_TARGET,
	RW_CLUSTER,
	SCREENING_ORIENTATION,
	SCREEN_TYPE,
	TARGET_RATIONALE,
	PROJECT_GLOBAL_OBJECTIVE,
	SOURCE_SYSTEM,
	CREATIONDATE_DT,
	LASTUPDATEDATE_DT,
	CREATEDBY,
	UPDATEDBY,
	SOURCE_OF_ORIGIN,
	STATE
) as select * from landing.mdm_project_master
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MDM_PROJECT_MASTER successfully created")
                elif "already exists" in message:
                    print("VW_MDM_PROJECT_MASTER view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MDM_PROJECT_MASTER: {e}")
        #Handle error  
def create_stg_manual_inputs_views():
    cur=_conn_adam()    
    cur.execute("""use schema sales.stg_manual_inputs""")
    print("\n-----------view Creation Starts for schema stg_manual_inputs-------------------")
    try: 
        result=cur.execute("""create view if not exists ICD10_MEDDRA_MAPPING(
	ICD10_CHAPTER_NUMBER_2019_INTL_CORE_VER,
	ICD10_CHAPTER_2019_INTL_CORE_VER,
	ICD10_CODE_2019_INTL_CORE_VER,
	ICD10_TERM_2019_INTL_CORE_VER,
	MAPPED_MEDDRA_LLT,
	MAPPED_MEDDRA_LLT_CODE,
	MAP_ATTRIBUTE,
	MEDDRA_PT,
	MEDDRA_PT_CODE,
	MEDDRA_VER
    ) as select * from landing.ICD10_MEDDRA_MAPPING
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view ICD10_MEDDRA_MAPPING successfully created")
                elif "already exists" in message:
                    print("ICD10_MEDDRA_MAPPING view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view ICD10_MEDDRA_MAPPING: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists MEDDRA_SNOMED_CT_MAPPING(
	MEDDRA_LLT_CODE,
	MEDDRA_LLT,
	SNOMED_CT_CODE,
	SNOMED_CT_FSN
) as select * from landing.MEDDRA_SNOMED_CT_MAPPING
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view MEDDRA_SNOMED_CT_MAPPING successfully created")
                elif "already exists" in message:
                    print("MEDDRA_SNOMED_CT_MAPPING view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view MEDDRA_SNOMED_CT_MAPPING: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists PROJECT_TYPE(
	TPR_ID,
	TPR_CD,
	TPR_DESC,
	TPR_PRIME_TABLE,
	TPR_PRIME_CATEGORY,
	TPR_PRIME_PORTFOLIO,
	TPR_FIRST_CD,
	TPR_ORDER,
	UPDATE_DT,
	RW_UID,
	PROCESS_UID
) as select * from landing.PROJECT_TYPE
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view PROJECT_TYPE successfully created")
                elif "already exists" in message:
                    print("PROJECT_TYPE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view PROJECT_TYPE: {e}")
        #Handle error     
def create_crdh_dea_iport_reporting_views():
    cur=_conn_adam()    
    cur.execute("""use schema sales.crdh_dea_iport_reporting""")
    print("\n-----------view Creation Starts for schema crdh_dea_iport_reporting-------------------")
    try: 
        result=cur.execute("""create view if not exists PRTFL_TCP_PROFILE(
	TCP_PROF_ID,
	TITLE,
	"ATTRIBUTE NAME",
	INDICATION,
	"PROJECT CODE",
	"PROJECT NAME",
	COMMENTS,
	STATUS,
	"CREATED BY",
	"MODIFIED BY",
	CREATED,
	MODIFIED
) as select * from landing.PRTFL_TCP_PROFILE
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view PRTFL_TCP_PROFILE successfully created")
                elif "already exists" in message:
                    print("PRTFL_TCP_PROFILE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view PRTFL_TCP_PROFILE: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists PRTFL_TPP_PROFILE(
	TPP_PROF_ID,
	TITLE,
	"ATTRIBUTE NAME",
	INDICATION,
	"STANDARD OF CARE AT LAUNCH NAME",
	"BASE PROFILE",
	"COMPARATIVE POSITION",
	"STANDARD OF CARE",
	"UPSIDE PROFILE",
	"MINIMALLY MARKETABLE PROFILE",
	"PROJECT CODE",
	"PROJECT NAME",
	"MINIMALLY VS SOC",
	"UPSIDE VS SOC",
	STATUS,
	"CREATED BY",
	"MODIFIED BY",
	CREATED,
	MODIFIED,
	"SOC LAUNCH NAME 2",
	"SOC DESCRIPTION 2",
	"COMPARATIVE POSITION 2",
	"SOC COUNT",
	"SOC LAUNCH NAME 3",
	"SOC DESCRIPTION 3",
	"COMPARATIVE POSITION 3",
	"UPSIDE VS SOC 2",
	"UPSIDE VS SOC 3",
	"MINIMALLY VS SOC 2",
	"MINIMALLY VS SOC 3",
	"SOC DESCRIPTION",
	"SOC LAUNCH NAME",
	PHASE1,
	PHASE2,
	PHASE3,
	LATESTPUBLISHEDSOC
) as select * from landing.prtfl_tpp_profile
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view PRTFL_TPP_PROFILE successfully created")
                elif "already exists" in message:
                    print("PRTFL_TPP_PROFILE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view PRTFL_TPP_PROFILE: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists PRTFL_TVP_PROFILE(
	TVP_PROF_ID,
	TITLE,
	"ATTRIBUTE NAME",
	INDICATION,
	"PROJECT CODE",
	"PROJECT NAME",
	COMMENTS,
	STATUS,
	"CREATED BY",
	"MODIFIED BY",
	CREATED,
	MODIFIED
) as select * from landing.PRTFL_TVP_PROFILE
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view PRTFL_TVP_PROFILE successfully created")
                elif "already exists" in message:
                    print("PRTFL_TVP_PROFILE view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view PRTFL_TVP_PROFILE: {e}")
        #Handle error
def create_dp_rdportfolio360_views():
    cur=_conn_adam()    
    cur.execute("""use schema sales.dp_rdportfolio360""")
    print("\n-----------view Creation Starts for schema dp_rdportfolio360-------------------")
    try: 
        result=cur.execute("""create view if not exists  VW_MEDDRA_ICD10_MAPPING(
	SANOFI_MEDDRA_INDICATION_CODE,
	ICD10_CODE_2019_INTL_CORE_VER,
	MEDDRA_PT_CODE,
	MEDDRA_LLT_CODE
) COMMENT='Maps MEDDRA codes to ICD10 codes for indications used in Sanofi Project Indications. This is filtered to Indications with a status of Ongoing, Completed, or Stopped and excludes the COMMON placeholder indication. The basis of this is the indication data in the R&D MDM and the mapping data from MedDRA'
 as
(select distinct indmdm.clinical_ind, icd10.icd10_code_2019_intl_core_ver, icd10.meddra_pt_code, icd10.mapped_meddra_llt_code
from SRV_MDM_RNDMASTERDATA.vw_mdm_project_ind_master indmdm
left join stg_manual_inputs.icd10_meddra_mapping icd10 on (icd10.meddra_pt_code = indmdm.clinical_ind or icd10.mapped_meddra_llt_code = indmdm.clinical_ind)
where indmdm.project_ind_status in ('Ongoing', 'Completed', 'Stopped')
and indmdm.clinical_ind not like 'COMM%')
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MEDDRA_ICD10_MAPPING successfully created")
                elif "already exists" in message:
                    print("VW_MEDDRA_ICD10_MAPPING view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MEDDRA_ICD10_MAPPING: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists  VW_MEDDRA_SNOMEDCT_MAPPING(
	CLINICAL_IND,
	MEDDRA_LLT_CODE,
	SNOMED_CT_CODE
) COMMENT='Maps MEDDRA codes to SNOMED CT codes for indications used in Sanofi Project Indications. This is filtered to Indications with a status of Ongoing, Completed, or Stopped and excludes the COMMON placeholder indication. The basis of this is the indication data in the R&D MDM and the SNOMED CT mapping data from MedDRA'
 as
(
select distinct indmdm.clinical_ind as clinical_ind, snomedct.meddra_llt_code as meddra_llt_code, snomedct.snomed_ct_code as SNOMED_CT_CODE
from SRV_MDM_RNDMASTERDATA.vw_mdm_project_ind_master indmdm
left join stg_manual_inputs.meddra_snomed_ct_mapping snomedct on snomedct.meddra_llt_code = indmdm.clinical_ind
where indmdm.project_ind_status in ('Ongoing', 'Completed', 'Stopped')
and indmdm.clinical_ind not like 'COMM%')
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_MEDDRA_SNOMEDCT_MAPPING successfully created")
                elif "already exists" in message:
                    print("VW_MEDDRA_SNOMEDCT_MAPPING view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_MEDDRA_SNOMEDCT_MAPPING: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""
        create view if not exists  VW_PROJECT_INDICATION_FLAT(
	PROJECT_CODE,
	PROJECT_CATEGORY,
	PROJECT_ORGANIZATION,
	PROJECT_NAME,
	PROJECT_DESCRIPTION,
	PROJECT_STATUS,
	PROJECT_PHASE,
	PROJECT_PRIORITY,
	PROJECT_INNOVATION_STATUS,
	PROJECT_RESEARCH_DEVELOPMENT_LINK,
	PROJECT_SANOFI_THERAPEUTIC_AREA,
	ASSET_INN,
	ASSET_BRAND_NAME,
	ASSET_MECHANISM_OF_ACTION,
	ASSET_MOA_SHORT_NAME,
	ASSET_ACTIVE_SUBSTANCE_TYPE,
	ASSET_ACTIVE_SUBSTANCE_SUBTYPE,
	ASSET_ORIGIN_OF_ACTIVE_SUBSTANCE,
	ASSET_PHARMACOLOGICAL_EFFECT,
	INDICATION_UNIQUE_CODE,
	INDICATION_LEAD_FLAG,
	INDICATION_LONGNAME,
	INDICATION_SHORTNAME,
	INDICATION_PHASE,
	INDICATION_CODE_MEDDRA,
	INDICATION_NAME_MEDDRA,
	INDICATION_STATUS,
	INDICATION_SANOFI_THERAPEUTIC_AREA,
	INDICATION_SANOFI_SUB_THERAPEUTIC_AREA_FRANCHISE,
	INDICATION_PTRS,
	LAST_PROJECT_INDICATION_GATE_MILESTONE,
	LAST_PROJECT_INDICATION_GATE_MILESTONE_DATE,
	NEXT_PROJECT_INDICATION_GATE_MILESTONE,
	NEXT_PROJECT_INDICATION_GATE_MILESTONE_DATE,
	GOV_APPROVED_PHASE_1_POS,
	GOV_APPROVED_PHASE_2A_POS,
	GOV_APPROVED_PHASE_2B_POS,
	GOV_APPROVED_PHASE_2_POS,
	GOV_APPROVED_PHASE_3_POS,
	LAST_REFRESH_DATE
) as (
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
  )
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_INDICATION_FLAT successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_INDICATION_FLAT view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_INDICATION_FLAT: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists  VW_PROJECT_INDICATION_MILESTONE_DATES(
	PROJECT_CODE,
	INDICATION_UNIQUE_CODE,
	LAST_MILESTONE,
	LAST_MILESTONE_PLANNED_FINISH_DT,
	NEXT_MILESTONE,
	NEXT_MILESTONE_PLANNED_FINISH_DT
) COMMENT='The view contains records of project indication milestones, specifically milestone types and planned completion dates. Currently this data set only has the submission/approval milestones for the 4 major Sanofi regions of USA (US), Europe (EU), China (CN), and Japan (JP) as this is what is tracked in RDPM. Each record represents a single milestone type for a given project indication, including the First Submission and First Approval milestones (for which the associated region/country can be cound in the MILESTONE_COUNTRY_CODE column. The only exceptions to this are the \"Submission\" and \"Approval\" milestones. For the \"Submission\" and \"Approval\" milestones, there will be one record per Project Indication \"Submission\" or \"Approval\" for each of the remaining three region/countries that Sanofi plans to submit marketing authorization for. The milestone types present are Target Selection - M0, Lead Selection - M1, Proof of Mechanism, Pre Candidate Selection, Proof of Concept, Start Development - M2, Proof of Commercial Concept, Start Ph01, GNG Ph02, GNG Ph2A, Start Ph02, Start Ph2A, GNG Ph2B, Start Ph2B, GNG Ph03, Start Ph03,First Submission, First Approval, Submission, Approval'
 as


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
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_INDICATION_MILESTONE_DATES successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_INDICATION_MILESTONE_DATES view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_INDICATION_MILESTONE_DATES: {e}")
        #Handle error

    try: 
        result=cur.execute("""create view if not exists  VW_PROJECT_INDICATION_READOUTS_MILESTONES(
	PROJECT_CODE,
	INDICATION_UNIQUE_CODE,
	READOUT_NAME,
	READOUT_PLANNED_DT
) COMMENT='View containing upcoming project readout milestones for ongoing R&D projects. Includes readouts planned for the current year and next year only. Filters for active projects in research, development, and vaccine organizations across all clinical phases.'
 as
   (
    SELECT 
        PRJMDM.PROJECT_CODE_CD      AS PROJECT_CODE, 
        WBS.IND_FUNCTIONAL_ID       AS INDICATION_UNIQUE_CODE, 
        TSK.TSK_PFM_DESC            AS READOUT_NAME, 
        TSK.TSK_PLANNED_FINISH_DT   AS READOUT_PLANNED_DT
    FROM SRV_RND_DF.VW_TASK TSK
    INNER JOIN SRV_RND_DF.MVW_WBS_HIERARCHY WBS 
        ON WBS.WBS_ID             = TSK.TSK_WBS_ID 
        AND WBS.TIME_ID           = TSK.TIME_ID
    INNER JOIN SRV_MDM_RNDMASTERDATA.VW_MDM_PROJECT_MASTER PRJMDM 
        ON PRJMDM.PROJECT_CODE_CD = WBS.PRJ_FUNCTIONAL_ID
    INNER JOIN SRV_RND_DF.VW_REF_BASELINE BAS 
        ON BAS.TIME_ID            = WBS.TIME_ID 
        AND BAS.BAS_DESC          = 'Live'
    WHERE TSK.IS_LAST = TRUE
        AND PRJMDM.PROJECT_CATEGORY            IN ('R','D')
        AND PRJMDM.PROJECT_ORGANIZATION_TYPE   IN ('RESEARCH', 'DEVELOPMENT', 'VACCINE')
        AND PRJMDM.PROJECT_STATUS              = 'Ongoing'
        AND PRJMDM.PROJECT_PHASE               IN  ('M0-M1','M1-M2','M0-M2','Preclinical','Phase 1','Phase 2','Phase 2A','Phase 2B','Phase 3','Regulatory submission','LCM')
        AND (YEAR(TSK.TSK_PLANNED_FINISH_DT)   = YEAR(CURRENT_DATE) 
		    OR YEAR(TSK.TSK_PLANNED_FINISH_DT) = YEAR(CURRENT_DATE) + 1)
    ORDER BY  
        READOUT_PLANNED_DT, 
        PROJECT_CODE, 
        INDICATION_UNIQUE_CODE
    );
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_INDICATION_READOUTS_MILESTONES successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_INDICATION_READOUTS_MILESTONES view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_INDICATION_READOUTS_MILESTONES: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists  VW_PROJECT_INDICATION_TPP(
	TPP_SYS_ID,
	PROJECT_CODE,
	INDICATION_UNIQUE_CODE,
	TPP_SOC_CATEGORY,
	TPP_SOC_SUBCATEGORY,
	TPP_BASE_PROFILE_SOC_FOR_SUBCATEGORY,
	TPP_UPSIDE_PROFILE_SOC_FOR_SUBCATEGORY,
	TPP_MINIMALLY_MARKETABLE_PROFILE_SOC_FOR_SUBCATEGORY,
	TPP_COMPARATOR_PRODUCT1_NAME,
	TPP_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
	TPP_BASE_VS_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
	TPP_UPSIDE_VS_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
	TPP_MINIMALLY_MARKETABLE_VS_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
	TPP_COMPARATOR_PRODUCT2_NAME,
	TPP_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
	TPP_BASE_VS_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
	TPP_UPSIDE_VS_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
	TPP_MINIMALLY_MARKETABLE_VS_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
	TPP_COMPARATOR_PRODUCT3_NAME,
	TPP_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
	TPP_BASE_VS_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
	TPP_UPSIDE_VS_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
	TPP_MINIMALLY_MARKETABLE_VS_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
	TPP_STATUS,
	TPP_CREATED_DATE,
	TPP_MODIFIED_DATE
) COMMENT='This view integrates TPP data from iPORT with Indication data from RDPM. It is a flattened out structure for the TPP with a workaround in place to account for the iPORT design that stores TPPs with Indication Shortnames instead of Indication Codes. A second workaround is that the query retrieves the Indication Unique Code from the RDPM data instead of the MDM data because in the current setup, the Indication history is not shared from the MDM system to the Asset Portfolio Data Fabric. That said, since Indications are authored in RDPM and then fed to the MDM, this should not cause an issue until a more robust solution using MDM as the source of truth can be put in place.'
 as
(
WITH max_time_id AS (
  SELECT
    ind_unique_cd,
    MAX(time_id) AS max_time_id
  FROM
    srv_rnd_df.vw_indication
  WHERE
    NOT ind_shortname IS NULL
  GROUP BY
    ind_unique_cd
),
latest_indication AS (
  SELECT
    indrdpm.ind_unique_cd,
    indrdpm.ind_shortname,
    indrdpm.time_id
  FROM
    srv_rnd_df.vw_indication AS indrdpm
    JOIN max_time_id ON indrdpm.ind_unique_cd = max_time_id.ind_unique_cd
    AND indrdpm.time_id = max_time_id.max_time_id
)

SELECT
  tpp.tpp_prof_id as TPP_SYS_ID,
  tpp."Project Code" as PROJECT_CODE,
  case when latest_indication.ind_unique_cd is null then tpp.indication
  else latest_indication.ind_unique_cd end as INDICATION_UNIQUE_CODE,
  tpp.title as TPP_SOC_CATEGORY,
  tpp."Attribute Name" as TPP_SOC_SUBCATEGORY,
  tpp."Base Profile" as TPP_BASE_PROFILE_SOC_FOR_SUBCATEGORY,
  tpp."Upside Profile" as TPP_UPSIDE_PROFILE_SOC_FOR_SUBCATEGORY,
  tpp."Minimally Marketable Profile" as TPP_MINIMALLY_MARKETABLE_PROFILE_SOC_FOR_SUBCATEGORY,
  tpp."SOC Launch Name" as TPP_COMPARATOR_PRODUCT1_NAME,
  tpp."SOC Description" as TPP_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
  tpp."Comparative Position" as TPP_BASE_VS_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
  tpp."upside vs soc" as TPP_UPSIDE_VS_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
  tpp."minimally vs soc" as TPP_MINIMALLY_MARKETABLE_VS_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
  tpp."SOC Launch Name 2" as TPP_COMPARATOR_PRODUCT2_NAME,
  tpp."SOC Description 2" as TPP_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
  tpp."Comparative Position 2" as TPP_BASE_VS_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
  tpp."Upside vs SOC 2" as TPP_UPSIDE_VS_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
  tpp."Minimally vs SOC 2" as TPP_MINIMALLY_MARKETABLE_VS_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
  tpp."SOC Launch Name 3" as TPP_COMPARATOR_PRODUCT3_NAME,
  tpp."SOC Description 3" as TPP_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
  tpp."Comparative Position 3" as TPP_BASE_VS_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
  tpp."Upside vs SOC 3" as TPP_UPSIDE_VS_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
  tpp."Minimally vs SOC 3" as TPP_MINIMALLY_MARKETABLE_VS_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
  tpp.status as TPP_STATUS,
  tpp.created as TPP_CREATED_DATE,
  tpp.modified as TPP_MODIFIED_DATE
  
FROM
  crdh_dea_iport_reporting.prtfl_tpp_profile AS tpp
  LEFT JOIN latest_indication ON tpp.indication = latest_indication.ind_shortname
  AND LEFT (
    latest_indication.ind_unique_cd,
    LENGTH (latest_indication.ind_unique_cd) - 7
  ) = tpp."Project Code"
where tpp.indication is not null  
ORDER BY
  tpp.tpp_prof_id)
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_INDICATION_TPP successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_INDICATION_TPP view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_INDICATION_TPP: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists  VW_PROJECT_TCP(
	TCP_ID,
	PROJECT_CODE,
	PROJECT_NAME,
	TCP_CHARACTERISTIC,
	TCP_CHARACTERISTIC_VALUE,
	TCP_STATUS,
	TCP_CREATED_BY,
	TCP_MODIFIED_BY,
	TCP_CREATED_DATE,
	TCP_MODIFIED_DATE
) COMMENT='View containing TCP (Target Candidate Profile) data from the Portfolio TCP Profile table. Includes only records with status of Published or Draft.'
 as
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
        );
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_TCP successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_TCP view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_TCP: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists  VW_PROJECT_TEAM_MEMBER(
	PROJECT_CODE,
	INDICATION_UNIQUE_CODE,
	PROJECT_TEAM_MEMBER_TEAMS,
	PROJECT_TEAM_MEMBER_PROJECT_ROLE_ORIG,
	PROJECT_TEAM_MEMBER_DESC,
	PROJECT_TEAM_MEMBER_EMAIL,
	PROJECT_TEAM_MEMBER_SUB_TEAMS,
	PROJECT_TEAM_MEMBER_DEPARTMENT_CODE,
	PROJECT_TEAM_MEMBER_FUNCTION,
	PROJECT_TEAM_MEMBER_SCOPE_DESC,
	PROJECT_TEAM_MEMBER_PROJECT_ROLE
) COMMENT='The view showing Live baseline data containsTeam member information from RDPM for projects and Indication across R&D(including pharma & Vaccine) for Iport Reporting'
 as 
select * from (
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
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_TEAM_MEMBER successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_TEAM_MEMBER view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_TEAM_MEMBER: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists  VW_PROJECT_TCP(
	TCP_ID,
	PROJECT_CODE,
	PROJECT_NAME,
	TCP_CHARACTERISTIC,
	TCP_CHARACTERISTIC_VALUE,
	TCP_STATUS,
	TCP_CREATED_BY,
	TCP_MODIFIED_BY,
	TCP_CREATED_DATE,
	TCP_MODIFIED_DATE
) COMMENT='View containing TCP (Target Candidate Profile) data from the Portfolio TCP Profile table. Includes only records with status of Published or Draft.'
 as
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
        );
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_TCP successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_TCP view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_TCP: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists  VW_PROJECT_TEAM_MEMBER(
	PROJECT_CODE,
	INDICATION_UNIQUE_CODE,
	PROJECT_TEAM_MEMBER_TEAMS,
	PROJECT_TEAM_MEMBER_PROJECT_ROLE_ORIG,
	PROJECT_TEAM_MEMBER_DESC,
	PROJECT_TEAM_MEMBER_EMAIL,
	PROJECT_TEAM_MEMBER_SUB_TEAMS,
	PROJECT_TEAM_MEMBER_DEPARTMENT_CODE,
	PROJECT_TEAM_MEMBER_FUNCTION,
	PROJECT_TEAM_MEMBER_SCOPE_DESC,
	PROJECT_TEAM_MEMBER_PROJECT_ROLE
) COMMENT='The view showing Live baseline data containsTeam member information from RDPM for projects and Indication across R&D(including pharma & Vaccine) for Iport Reporting'
 as 
select * from (
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
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_TEAM_MEMBER successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_TEAM_MEMBER view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_TEAM_MEMBER: {e}")
        #Handle error
        
    try: 
        result=cur.execute("""create view if not exists VW_PROJECT_TVP(
	PROJECT_CODE,
	INDICATION_UNIQUE_CODE,
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
) COMMENT='View containing aggregated TVP (Target Value Proposition) data from the Portfolio TVP Profile table. Aggregates multiple TVP attributes by Project Code and Indication, including populations of interest, needs, competitive positioning, and value propositions for prescribers, patients, and payers. Includes only records with status of Published, Draft, or Publish.'
 as
(
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
        FROM SALES.CRDH_DEA_IPORT_REPORTING.PRTFL_TVP_PROFILE
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
)
    """)
        status=result.fetchone()
        if status:
                message=status[0]
                message=message.lower()
                if "successfully created" in message:
                    print("view VW_PROJECT_TVP successfully created")
                elif "already exists" in message:
                    print("VW_PROJECT_TVP view already exists, skipped creation")
    except Exception as e:
        print(f"Error creating view VW_PROJECT_TVP: {e}")
        #Handle error
        
accountadmin_task()       
create_db_schemas()
create_tables()
create_file_format()
create_local_stage()
create_srv_rnd_df_views()
create_srv_mdm_rndmasterdata_views()
create_stg_manual_inputs_views()
create_crdh_dea_iport_reporting_views()
create_dp_rdportfolio360_views()

