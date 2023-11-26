from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import yaml
from importlib.machinery import SourceFileLoader
from load_to_db import load

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

def create_dags_from_yml(yaml_path: str) -> DAG:
    with open(yaml_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    # dag name
    dag_id = list(config.keys())[0]
    config = config[dag_id]

    # default parameters
    owner = config.get('owner', 'Airflow')
    description = config.get('descriptsion', 'None')
    current_date = datetime.now()
    start_date = config.get('start_date', current_date)
    schedule_interval = config.get('schedule_interval', '0 9 * * *')
    url = config.get('url')
    catchup = config.get('catchup', False)

    email_on_failure = config.get('email_on_failure', False)
    email = config.get('email', False)

    # python functions file
    python_callable_file = config.get('python_callable_file')
    python_callable_file_path = os.path.join(dags_directory, python_callable_file)

    # files
    file_extension = config.get('tasks').get('extract').get('file_extension', 'csv')
    timestamp = '{{ ds }}_{{ ts }}'  # Use the execution date as a timestamp
    output_filename = f'staging_data/{dag_id}_{timestamp}.{file_extension}'
    output_filename_transformed = f'staging_data/{dag_id}_{timestamp}_transformed.{file_extension}'

    # import the python_callable module dynamically
    module_name = os.path.splitext(os.path.basename(python_callable_file_path))[0]
    module = SourceFileLoader(module_name, os.path.abspath(python_callable_file_path)).load_module()

    # extract
    extract_python_callable = config.get('tasks').get('extract').get('python_callable')
    retries = config.get('tasks').get('extract').get('retries', 0)
    retry_delay = config.get('tasks').get('extract').get('retry_delay', 1200)
    extract_function = getattr(module, 'extract')
    def extract_wrapper(url, output_filename):
        return extract_function(url, output_filename)

    # transform
    transform_python_callable = config.get('tasks').get('transform').get('python_callable')
    transform_dependencies = config.get('tasks').get('transform').get('dependencies')
    transform_function = getattr(module, 'transform')
    def transform_wrapper(input_filename, output_filename):
        return transform_function(input_filename, output_filename)

    # load
    load_dependencies = config.get('tasks').get('load').get('dependencies')
    mode = config.get('tasks').get('load').get('mode')
    dataset_name = config.get('tasks').get('load').get('dataset_name', dag_id)
    fields = config.get('tasks').get('load').get('fields')
    def load_wrapper(dataset_name, input_filename, fields, mode):
        return load(dataset_name, input_filename, fields, mode)

    # DAG
    default_args = {
        'owner': owner,
        'start_date': start_date,
        'schedule_interval': schedule_interval,
        'retries': 0,
        'catchup': catchup,
        'email_on_failure': email_on_failure,
        'email': email
    }

    with DAG(
        dag_id=dag_id,
        default_args=default_args,
        description=description,
    ) as dag:
        extract_task = PythonOperator(
            task_id=extract_python_callable,
            python_callable=extract_wrapper,
            retries=retries,
            retry_delay=retry_delay,
            op_kwargs=dict(
                url=url,
                output_filename=output_filename
            )
        )
        transform_task = PythonOperator(
            task_id=transform_python_callable,
            python_callable=transform_wrapper,
            op_kwargs=dict(
                input_filename=output_filename,
                output_filename=output_filename_transformed
            )
        )
        load_task = PythonOperator(
            task_id='load',
            python_callable=load_wrapper,
            op_kwargs=dict(
                dataset_name=dataset_name,
                input_filename=output_filename_transformed,
                fields=fields,
                mode=mode
            )
        )

    extract_task >> transform_task >> load_task

for yml_file in yml_files:
    create_dags_from_yml(yml_file)
