import pandas as pd
import os

csv_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))+'/source_files/csv/consumer_input_files/Masking_Inputs.csv'
xls_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))+'/source_files/xls/p360_Making_Controls.xlsx'
sheet_name='column_access'

def convert_xls_to_csv(xls_file, csv_file, sheet_name):
  try:
    df = pd.read_excel(xls_file, sheet_name=sheet_name, engine='xlrd')
    df.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"Successfully converted '{xls_file}' to '{csv_file}'")
  except Exception as e:
    print(f"An error occurred: {e}")
    
convert_xls_to_csv(xls_file, csv_file,sheet_name)