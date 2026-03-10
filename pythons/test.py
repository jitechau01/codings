import os
import pandas as pd
file=os.path.dirname(os.path.dirname(__file__))+'/source_files/csv/consumer_input_files/data_classification.xlsx'
import sys
sys.path.insert(1,'/home/cloud/codings/pythons')
from __con_policy_admin import _conn

cur=_conn()

df = pd.read_excel(file)
TAG_NAME = "DATA_SENSITIVITY"
for _, row in df.iterrows():

    sensitivity = row["SENSITIVITY_LEVEL"]
    view_name = row["VIEW_NAME"]
    columns = row["COLUMN_NAME"]
    
    print(sensitivity,view_name,columns)

    # skip empty rows
    # if pd.isna(sensitivity) or pd.isna(view_name) or pd.isna(columns):
    #     continue

    # split column list
    # column_list = [c.strip() for c in str(columns).split(",")]
    
    # print(column_list)
    
    # for col in column_list:
    #     sql = f"""ALTER VIEW {view_name} MODIFY COLUMN {col} SET TAG {TAG_NAME} = '{sensitivity}' """
    
    # try:
    #     print(sql)
    #     cur.execute(sql)
    # except Exception as e:
    #         print(f"Error applying tag on {view_name}.{col}: {e}")

# print("Tagging completed.")