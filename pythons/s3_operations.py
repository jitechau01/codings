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
key='parquet/'

def s3_client():return boto3.client('s3')

def s3_resource():return boto3.resource('s3')

def create_bucket(bucket_name):
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket=bucket_name)
        
def delete_bucket(bucket_name):
    s3 = s3_client()
    s3.delete_bucket(Bucket=bucket_name)
        
def upload_file_to_s3():
    s3 = s3_client()
    for file in files_list:
        file_name = os.path.basename(file)
        s3.upload_file(file, bucket_name, key+file_name)
        
def list_buckets():
    s3 = s3_client()
    response = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    for bucket in buckets:
        print(f'Bucket Name: {bucket}')
        
def list_files_in_bucket(bucket_name):
    s3 = s3_client()
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f'File Name: {obj["Key"]}')
    else:
        print('No files found in the bucket.')

#create_bucket(bucket_name)
#delete_bucket(bucket_name)
#print(list_buckets())
#upload_file_to_s3()
#list_buckets()
#list_files_in_bucket(bucket_name)