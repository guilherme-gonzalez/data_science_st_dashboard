from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import os
import boto3

# Authenticate with Kaggle API
api = KaggleApi()
api.authenticate()

# Download the dataset
dataset = 'arnabchaki/data-science-salaries-2023'
api.dataset_download_files(dataset)

# Unzip the downloaded file
with zipfile.ZipFile('data-science-salaries-2023.zip', 'r') as zip_ref:
    zip_ref.extractall('data-science-salaries-2023')

print("Download and extraction completed!")

#Setup bucket with boto3
s3resource=boto3.client('s3','us-east-1')
s3resource.create_bucket(Bucket='s3kaggledatasets')

print("Bucket created in s3!")