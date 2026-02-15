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
    
def adam_task():
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
        result=cur.execute("""create or replace view MVW_WBS_HIERARCHY(
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
    
# accountadmin_task()       
# adam_task()
# create_tables()
# create_file_format()
# create_local_stage()
create_srv_rnd_df_views()

