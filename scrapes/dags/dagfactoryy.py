import os

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

import yaml


for yml_file in yml_files:
    with open(yml_file, 'r') as config_file:
            config = yaml.safe_load(config_file)

    dag_id = list(config.keys())[0]
    config = config[dag_id]

    fields = config.get('tasks').get('load').get('fields')
    print(fields)