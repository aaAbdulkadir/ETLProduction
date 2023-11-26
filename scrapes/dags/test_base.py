import yaml
import os
import sys
import unittest

from load_to_db import load



class Test(unittest.TestCase):

    def validate_config(self, config_file_path):
        with open(config_file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        dag_id = list(config.keys())[0]
        config = config[dag_id]

        required_values = [
            'url', 'python_callable_file',
            'tasks.extract.python_callable', 'tasks.transform.python_callable',
            'tasks.load.mode', 'tasks.load.fields'
        ]

        for value in required_values:
            nested_keys = value.split('.')
            nested_value = config
            for key in nested_keys:
                nested_value = nested_value.get(key)
                if nested_value is None or nested_value == '':
                    self.fail(f"Value '{value}' is empty or missing in the YAML configuration.")
        
    def validate_load(self, config_file_path, input_filename):
        with open(config_file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)

        dag_id = list(config.keys())[0]
        config = config[dag_id]
        load = config.get('tasks').get('load')

        dataset_name = load['dataset_name']
        input_filename = 'testing.csv'
        fields = load['fields']
        mode = load['mode']

        # load(
        #     dataset_name,
        #     input_filename,
        #     fields,
        #     mode
        # )
        # print(load)
