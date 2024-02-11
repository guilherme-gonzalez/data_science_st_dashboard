# Data science salaries dashboard
In this project I'm going to import a kaggle dataset through the API, export it to s3, analyze and clean it, and finally build streamlit python dashboard.

## Steps:
Install kaggle, aws cli and boto3 in your CLI
```
pip install kaggle
```
```
pip install awscli
```
```
pip install boto3
```

## 1 .Create kaggle token
Going to Kaggle => Accounts => API => create token.

After setting up the token it generates a json file in this path:
```
/Users/USERNAME/.kaggle/kaggle.json
```

## 2. Generate AWS access key
Assuming you have an IAM user, go to IAM => Users => *IAMUSERNAME* => create access key.

then run this command in your CLI
```
aws configure
```
it should ask you to input this data:
```
AWS Access Key ID [None]: 
AWS Secret Access Key [None]: 
Default region name [None]: 
Default output format [None]: 
```
Fill in the access keys, region, and choose output format as json.

It's gonna output this two files:

![img](/Screenshot%202023-11-19%20at%201.19.42 AM.png)

## 2. Get kaggle dataset using the kaggle API
```python
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
```

## 3. Export dataset to s3
```python
import boto3
# Setup variables
dataset = 'data-science-salaries-2023/ds_salaries.csv'
s3kaggledatasets = 'arn:aws:s3:us-east-1:311598230231:accesspoint/accesspoint1'
s3_ds_salaries = 'ds_salaries.csv'
# Upload data
s3resource=boto3.client('s3','us-east-1')
s3resource.upload_file(dataset,s3kaggledatasets,s3_ds_salaries)

print("csv file sucessfully uploaded to s3!")
```

## 4. Analyze and clean s3 dataset using a notebook
We are mostly doing some exploratory data analysis using polars so we know what we are working with, and also doing some transformations so that de dashboard visualization comes out looking cleaner.

## 5. build a dashboard mockup using excalidraw.com
![img](/Untitled-2024-01-20-2119.png)

## 6. build dashboard using streamlit

