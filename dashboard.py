import streamlit as st
import pandas as pd
import boto3
from io import StringIO
import matplotlib.pyplot as plt
from streamlit_card import card

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

# Set page layout
st.set_page_config(layout="wide")
st.title('Data science salaries 2020-2023')

# Get unique job groups
job_groups = df['job_group'].unique()

#count(*) jobs, avg(salary_in_usd)
salary = df['salary_in_usd']
avg_salary = salary.mean()
count_jobs = df.count()

# Get unique values for each slicer and add 'All' option
experience_levels = ['All'] + df['_experience_level'].unique().tolist()
remote_ratios = ['All'] + df['_remote_ratio'].unique().tolist()
company_sizes = ['All'] + df['company_size'].unique().tolist()
employment_types = ['All'] + df['_employment_type'].unique().tolist()
job_roles = ['All'] + df['job_group'].unique().tolist()

# Create select boxes in the sidebar for slicers
slc_experience_level = st.sidebar.selectbox('Select Experience Level', experience_levels)
slc_remote_ratio = st.sidebar.selectbox('Select Remote Ratio', remote_ratios)
slc_company_size = st.sidebar.selectbox('Select Company Size', company_sizes)
slc_employment_type = st.sidebar.selectbox('Select Employment Type', employment_types)
slc_job_group = st.sidebar.selectbox('Select Job Role', job_roles)

# Filter the dataframe based on the selected slicers
if (slc_experience_level == 'All' and slc_remote_ratio == 'All' and slc_company_size == 'All'
    and slc_employment_type == 'All' and slc_job_group == 'All'):
    df_filtered = df  # Display all data
else:
    conditions = (
        (slc_experience_level == 'All' or df['_experience_level'] == slc_experience_level) &
        (slc_remote_ratio == 'All' or df['_remote_ratio'] == slc_remote_ratio) &
        (slc_company_size == 'All' or df['company_size'] == slc_company_size) &
        (slc_employment_type == 'All' or df['_employment_type'] == slc_employment_type) &
        (slc_job_group == 'All' or df['job_group'] == slc_job_group)
    )
    df_filtered = df[conditions]

# Create columns
col1, col2 = st.columns(2)

# Card for average salary
with col1:
    avg_salary_filtered = df_filtered['salary_in_usd'].mean()
    st.metric(label="Number of Jobs", value="{:,}".format(df_filtered.shape[0]))

# Card for job count - Centered
with col2:
    st.metric(label="Average Salary", value="${:,.2f}".format(avg_salary_filtered))


# Create the bar chart
with col1:
    plt.figure(figsize=(10,6))

    # For each job group, calculate the mean salary and plot
    for job in job_groups:
        avg_salary = df_filtered[df_filtered['job_group'] == job]['salary_in_usd'].mean()
        plt.barh(job, avg_salary, color='red')

    plt.title('Average salary_in_usd by job_group')
    plt.ylabel('Job Group')
    plt.xlabel('Average Salary in USD')

    # Use Streamlit's pyplot() function to display the plot
    st.pyplot(plt)

# Create the boxplot
with col2:
    plt.figure(figsize=(10,6))
    plt.boxplot([df_filtered[df_filtered['job_group'] == job]['salary_in_usd'] for job in job_groups], labels=job_groups, vert=False)
    plt.title('Boxplot of salary_in_usd by job_group')
    plt.ylabel('Job Group')
    plt.xlabel('Salary in USD')

    # Use Streamlit's pyplot() function to display the plot
    st.pyplot(plt)

# Display the filtered dataframe
st.dataframe(df_filtered)