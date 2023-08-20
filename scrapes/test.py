import psycopg2
from psycopg2 import sql
import os
import json
import yaml

dags_directory = os.path.dirname(__file__)
dag_folders = [
    folder for folder in os.listdir(dags_directory) if os.path.isdir(os.path.join(dags_directory, folder))
]

yml_files = []

for dag_folder in dag_folders:
    dag_folder_path = os.path.join(dags_directory, dag_folder)
    yml_files += [
        os.path.join(dag_folder_path, file) for file in os.listdir(dag_folder_path) if file.endswith('.yml')
    ]

with open('dags/dummy_dag/dummy_dag.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

dag_id = list(config.keys())[0]
config = config[dag_id]

fields = config.get('tasks').get('load').get('fields')

create_table_query = f"CREATE TABLE IF NOT EXISTS table ("
for field in fields:
    field_name = field['name']
    field_type = field['type']
    create_table_query += f", {field_name} {field_type}"
create_table_query += ");"

print(fields)
column_names = ', '.join([field['name'] for field in fields])
print(column_names)

import pandas as pd

df = pd.read_csv('staging_data/dummy_dag_2023-08-20_2023-08-20T19:38:29.826554+00:00.csv')
print(df)
print(df.dtypes)