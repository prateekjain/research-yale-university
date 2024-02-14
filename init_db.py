import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname='researchDB',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)


# mz_values = []
# table_name = 'mz_value'

# for i in mz_values:
#     # Create a cursor
#     with conn.cursor() as cursor:
#         # Generate the parameterized query
#         query = f"INSERT INTO {table_name} (mz) VALUES ({i});"

#         # Execute the query with the array of values
#         cursor.execute(query)

# conn.commit()
# conn.close()


# for output files 2 column names are the same of HMDB_matches

def read_csv_with_encoding(csv_path, encodings):
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=encoding)
            return df
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(
        "Unable to decode CSV file with specified encodings")


tableName = "tumor_tumor_compare"
# Specify the path to your CSV file
csv_path = 'D:/Akshat/Project of python/research/normalvstumor_hilic_all/Tumor_tumor_test.csv'

encodings_to_try = ['utf-8', 'latin-1']  # Add more if needed

df = read_csv_with_encoding(csv_path, encodings_to_try)
# Read the CSV file and get column names
# df = pd.read_csv(csv_path)
print(df.columns)
df.columns = [col.replace(' - ', '_vs_').replace(
    '(', '_').replace(')', '_').replace('/', '_') for col in df.columns]

column_names = df.columns.tolist()
print(column_names)
column_names_fixed = [col.replace('.', '_').replace(
    '(', '_').replace(')', '_').replace('/', '_vs_') for col in column_names]

# Create a dynamic SQL statement to create the table
create_table_sql = f"CREATE TABLE {tableName} ({', '.join([f'{col} FLOAT' for col in column_names_fixed])});"

# Execute the SQL statement to create the table
with conn.cursor() as cursor:
    cursor.execute(create_table_sql)

# Specify the columns you want to alter to type TEXT
columns_to_alter = ["Metabolite"]

# add list_2_match, HMDB_matches_2 for output files too
# columns_to_alter = ["name", "HMDB_matches",
#                     "HMDB_matches_1", "list_2_match", "HMDB_matches_2"]


# # Create and execute ALTER TABLE statements
for col in columns_to_alter:
    alter_sql = f"ALTER TABLE {tableName} ALTER COLUMN {col} TYPE TEXT;"
    with conn.cursor() as cursor:
        cursor.execute(alter_sql)


# Load data into the table
with conn.cursor() as cursor:
    copy_sql = f"COPY {tableName} FROM '{csv_path}' DELIMITER ',' CSV HEADER;"
    cursor.execute(copy_sql)

# Commit changes and close the connection
conn.commit()
conn.close()
