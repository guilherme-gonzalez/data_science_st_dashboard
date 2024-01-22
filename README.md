# Data science salaries dashboard
```
Export kaggle dataset to s3 through the API and build streamlit python dashboard inside docker
```

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

## Create kaggle token
Going to Kaggle => Accounts => API => create token.

After setting up the token it generates a json file in this path:
```
/Users/USERNAME/.kaggle/kaggle.json
```

## Generate AWS access key
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

## Dashboard mockup 
![img](/Untitled-2024-01-20-2119.png)
