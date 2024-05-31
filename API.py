from flask import Flask, jsonify, request
from google.cloud import bigquery
import os

# Configure Flask app
app = Flask(__name__)

# Set up the credentials for the BigQuery client (assuming in root directory)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/serviceAccount.json"

# Set the project ID and dataset ID for the BigQuery table
project_id = "laboratory-385919"
dataset_id = "HRDB"
table_id = "department"

def query_data_all():
  """Fetches data from BigQuery and returns as a list of dictionaries."""
  client = bigquery.Client()
  QUERY = f"SELECT id, department FROM `{project_id}.{dataset_id}.{table_id}` order by 1 asc"
  query_job = client.query(QUERY)
  results = query_job.result()
  data = [dict(row) for row in results]  
  return data

def query_data(id):
    client = bigquery.Client()
    QUERY = f"SELECT id, department FROM `{project_id}.{dataset_id}.{table_id}` WHERE id = {id} order by 1 asc"
    query_job = client.query(QUERY)
    results = query_job.result()
    data = [dict(row) for row in results]  
    return data


def delete_department(id):
  client = bigquery.Client()
  QUERY = f"""
DELETE FROM `{project_id}.{dataset_id}.{table_id}` WHERE id = @id
"""
  query_job = client.query(QUERY.format(id=id))
  query_job.result()  # Wait for insert
  print(f"Deleted data where: id: {id}")
  return None
  

def insert_department(id, department):
  client = bigquery.Client()
  QUERY = f"""
INSERT INTO `{project_id}.{dataset_id}.{table_id}` (id, department)
VALUES (@id, @department)
"""
  query_job = client.query(QUERY.format(id=id, department=department))
  
  query_job.result()  # Wait for insert
  
  print(f"Inserted data: id: {id}, department: {department}")

  return None

#GET
@app.route('/departments')  # Define API route
def get_department():
  data = query_data_all()
  return jsonify(data)

@app.route('/departments/<int:id>', methods=['GET'])
def get_departments(id):
   data = query_data(id)
   return jsonify(data)


#http://127.0.0.1:5000/departments/ + json
#POST
@app.route('/departments', methods=['POST'])
def create_department():
    data = request.get_json()
    insert_department(data["id"],data["department"])


#http://127.0.0.1:5000/departments/1
#DELETE
@app.route('/departments/<int:id>', methods=['DELETE'])
def delete_department_by_id(id):
    try:
        delete_department(id)
        return jsonify({'message': f'Department with ID {id} deleted successfully'}), 200
    except Exception as e:
        # Handle potential exceptions during deletion
        return jsonify({'error': f'Error deleting department: {str(e)}'}), 500


if __name__ == '__main__':
  app.run(debug=True)  # Run Flask app in debug mode