import boto3
import glob
import os
from pathlib import Path

files_list=[]

source_files_path = Path(os.path.dirname(os.path.dirname((__file__)))+'/source_files/parquet')
parquet_files = glob.glob(os.path.join(source_files_path, "*.parquet"))
for file in parquet_files:
    files_list.append(file)


bucket_name = 'salesinputsource'

def s3_client():
    return boto3.client('s3')

def s3_resource():
    return boto3.resource('s3')

def create_bucket(bucket_name):
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket=bucket_name)
        
def delete_bucket(bucket_name):
    s3 = s3_client()
    s3.delete_bucket(Bucket=bucket_name)
        
def list_buckets():
    s3 = s3_client()
    response = s3.list_buckets()
    return [bucket['Name'] for bucket in response['Buckets']]

def upload_file(bucket_name, file_name, object_name=None):
    s3 = s3_client()
    if object_name is None:
        object_name = file_name
    s3.upload_file(file_name, bucket_name, object_name)

#create_bucket(bucket_name)
#delete_bucket(bucket_name)
#print(list_buckets())

for file in files_list:
    key='parquet/' + Path(file).name
    upload_file(bucket_name, file, object_name=key)