import os
import glob

filepath=os.path.dirname(os.path.dirname((__file__)))+'/source_files/parquet'

files=glob.glob(filepath+'/*.parquet')

for file in files:
    print(file)
