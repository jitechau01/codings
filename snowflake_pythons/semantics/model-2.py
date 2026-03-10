import os
import yaml
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_data_engineer import _conn

cur=_conn()

database = 'RNDCONTROLLING'
semantic_schema='semantic'
semantic_stage='istage'

stage_file_path = f"""@{database}.{semantic_schema}.{semantic_stage}/p360_Semantic_Model.yml"""
loccal_semantic_file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/source_files/yml/'
get_command = f"""GET {stage_file_path} file://{loccal_semantic_file_path}"""

# print(stage_file_path)
# print(local_download_path)
# print(get_command)

cur.execute(get_command)

print(f"File downloaded to {loccal_semantic_file_path}")