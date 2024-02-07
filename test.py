from sqlalchemy import select
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
# Function to fetch mz values from the database
db_url = os.getenv('DATABASE_URL')
print(db_url)


def get_case_columns_query(table_name, selected_mz):
    # Connect to the database
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    # Get all column names from the table
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    all_columns = [desc[0] for desc in cursor.description]
    print(all_columns)
    # Construct the SQL query dynamically
    query_case = f"SELECT {', '.join([col for col in all_columns if '_case' in col.lower()])} FROM {table_name} WHERE mz = {selected_mz}"
    query_control = f"SELECT {', '.join([col for col in all_columns if '_control' in col.lower()])} FROM {table_name} WHERE mz = {selected_mz}"
    
    # print(query_case)
    # print(query_control)
    # Close the cursor and connection
    cursor.close()
    connection.close()

    return query_case, query_control


selected_mz = '157.01199'  # replace with your actual value
table_name = 'asceding_output'  # replace with your actual table name

# Get the dynamic query
query_case, query_control = get_case_columns_query(table_name, selected_mz)

# Connect to the database
connection = psycopg2.connect(db_url)
cursor = connection.cursor()

# Execute the query
cursor.execute(query_case, (selected_mz,))
cursor.execute(query_control, (selected_mz,))

result = cursor.fetchall()

# Print or process the query result
print(result)

# Close the cursor and connection
cursor.close()
connection.close()