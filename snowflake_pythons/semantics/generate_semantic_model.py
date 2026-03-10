import os
import yaml
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_data_engineer import _conn
from varified_queries import verified_queries

database = "RNDCONTROLLING"
schema = "DP_RDPORTFOLIO360"
semantic_schema='semantic'
semantic_stage='istage'
Yml_file_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/source_files/yml'
cur=_conn()

def Create_Semantic_Model():

# ---------------------------
# Step 1 : Get all views
# ---------------------------

    cur.execute(f"SHOW VIEWS IN SCHEMA {database}.{schema}")

    views = [row[1] for row in cur.fetchall()]  # column 2 = view name

    tables = []

    # ---------------------------
    # Step 2 : Get columns of each view
    # ---------------------------

    for view in views:

        cur.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE
        FROM {database}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{schema}'
        AND TABLE_NAME = '{view}'
        """)

        columns = cur.fetchall()

        dimensions = []
        measures = []

        for col, dtype in columns:

            dtype = dtype.upper()

            if dtype in ["VARCHAR", "TEXT", "BOOLEAN", "DATE", "TIMESTAMP_NTZ"]:
                dimensions.append({
                    "name": col.lower(),
                    "expr": col,
                    "data_type": dtype.lower()
                })

            elif dtype in ["NUMBER", "FLOAT", "INT", "DECIMAL"]:
                measures.append({
                    "name": f"sum_{col.lower()}",
                    "expr": f"SUM({col})",
                    "data_type": "number"
                })

        table_block = {
            "name": view.lower(),
            "base_table": {
                "database": database,
                "schema": schema,
                "table": view
            },
            "dimensions": dimensions,
            "measures": measures
        }

        tables.append(table_block)

    # ---------------------------
    # Step 3 : Build semantic model
    # ---------------------------
    semantic_model = {
        "name": "portfolio360_semantic_model",
        "description": "This semantic data model contains comprehensive information about pharmaceutical  research and development projects, including their therapeutic indications, team members, and value propositions.  It allows analysis of medical coding mappings between different classification systems (like MedDRA and  ICD-10), project characteristics, therapeutic profiles, and team compositions. You can analyze project  statuses, therapeutic areas, mechanisms of action, and value assessments across different stakeholder  perspectives. The data enables tracking of project phases, priorities, and approved positions across  clinical development stages. You can also examine competitive positioning, patient populations of interest,  and value propositions for patients, payers, and prescribers",
        "tables": tables,
        "verified_queries": verified_queries

    }

    # ---------------------------
    # Step 4 : Write YAML
    # ---------------------------

    with open(f"""{Yml_file_path}/p360_Semantic_Model.yml""", "w") as f:
        yaml.dump(semantic_model, f, sort_keys=False)

    print("Semantic model generated successfully")
    print("Views processed:", len(views))

def Stage_Semantic_File():
    try:
        print(f"\n//Staging Semantic YML file {database}.{semantic_schema}.{semantic_stage}...")
        put_command = f"""PUT file://{Yml_file_path}/*.yml @{database}.{semantic_schema}.{semantic_stage} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"""
        cur.execute(put_command)
        print(f"    Semantic Model File staged successfully to @{database}.{semantic_schema}.{semantic_stage}")

    except Exception as e:
        print(f"Error: {e}")
        
Create_Semantic_Model()
Stage_Semantic_File()