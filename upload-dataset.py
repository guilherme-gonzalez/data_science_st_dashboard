import boto3
# Setup variables
dataset = 'data-science-salaries-2023/ds_salaries.csv'
s3kaggledatasets = 'arn:aws:s3:us-east-1:311598230231:accesspoint/accesspoint1'
s3_ds_salaries = 'ds_salaries.csv'
# Upload data
s3resource=boto3.client('s3','us-east-1')
s3resource.upload_file(dataset,s3kaggledatasets,s3_ds_salaries)

print("csv file sucessfully uploaded to s3!")
