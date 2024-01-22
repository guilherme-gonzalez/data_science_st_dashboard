import streamlit as st
import pandas as pd
import boto3
from io import StringIO
import matplotlib.pyplot as plt


# Load secrets
secrets = st.secrets["default"]

# Create a client
s3 = boto3.client(
    "s3",
    aws_access_key_id=secrets["aws_access_key_id"],
    aws_secret_access_key=secrets["aws_secret_access_key"],
    region_name=secrets["aws_default_region"]
)

# Get object from S3
obj = s3.get_object(Bucket="s3kaggledatasets", Key="output.csv")
body = obj['Body'].read()

# Create a dataframe
df = pd.read_csv(StringIO(body.decode('utf-8')))

# Get unique job groups
job_groups = df['job_group'].unique()

# Create a list to store data
data = []

# For each job group, filter the data and append to the list
for job in job_groups:
    data.append(df[df['job_group'] == job]['salary_in_usd'].tolist())

# Set page layout
st.set_page_config(layout="wide")
st.title('Data science salaries 2020-2023')

# Create columns
col1, col2 = st.columns(2)

# Create the bar chart
with col1:
    plt.figure(figsize=(10,6))

    # For each job group, calculate the mean salary and plot
    for job in job_groups:
        avg_salary = df[df['job_group'] == job]['salary_in_usd'].mean()
        plt.barh(job, avg_salary, color='red')

    plt.title('Average salary_in_usd by job_group')
    plt.ylabel('Job Group')
    plt.xlabel('Average Salary in USD')

    # Use Streamlit's pyplot() function to display the plot
    st.pyplot(plt)

# Create the boxplot
with col2:
    plt.figure(figsize=(10,6))
    plt.boxplot(data, labels=job_groups, vert=False)
    plt.title('Boxplot of salary_in_usd by job_group')
    plt.ylabel('Job Group')
    plt.xlabel('Salary in USD')

    # Use Streamlit's pyplot() function to display the plot
    st.pyplot(plt)

# Display the dataframe
st.dataframe(df)

# Get unique experience levels
experience_level = df['_experience_level'].unique()

# Create a select box in the sidebar for experience levels
slc_experience_level = st.sidebar.selectbox('Select Experience Level', experience_level)

# Filter the dataframe based on the selected experience level
df_filtered = df[df['_experience_level'] == slc_experience_level]

# Now use df_filtered in place of df for your plots and dataframe display
