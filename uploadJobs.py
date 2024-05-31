from google.cloud import bigquery
import os

# Set up the credentials for the BigQuery client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./credentials/serviceAccount.json"

# Create a BigQuery client
client = bigquery.Client()

# Set the project ID and dataset ID for the BigQuery table
project_id = "laboratory-385919"
dataset_id = "HRDB"
table_id = "jobs"

# Set the path to the CSV file
file_path = "./csvFiles/jobs.csv"

# Define the schema for the BigQuery table
schema = [
    bigquery.SchemaField("id", "INTEGER"),
    bigquery.SchemaField("jobs", "STRING"),
]

# Define the job configuration
job_config = bigquery.LoadJobConfig(
    schema=schema,
    skip_leading_rows=0,
    source_format=bigquery.SourceFormat.CSV,
)

# Set the table reference for the BigQuery table
table_ref = client.dataset(dataset_id).table(table_id)

# Load the data from the CSV file into the BigQuery table
with open(file_path, "rb") as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location="US",
        job_config=job_config,
    )

# Wait for the job to complete
job.result()

# Print the number of rows uploaded
print(f"Loaded {job.output_rows} rows into {table_ref.path}")