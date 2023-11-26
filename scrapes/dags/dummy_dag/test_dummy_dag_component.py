import os
import sys
import unittest
import pandas as pd

from dummy_dag_functions import (
    extract,
    transform
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from test_base import Test

class MyTest(Test):
    def setUp(self):
        self.working_dir =  os.path.dirname(__file__)
        self.config = os.path.join(
            self.working_dir, "dummy_dag.yml"
        )
        self.url = "https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"
        self.extracted_data = "test_data/extract_data.csv"
        self.transformed_data = "test_data/transformed_data.csv"

    def test_extract(self):
        output_filename = self.extracted_data
        extract(self.url, output_filename)

    def test_transform(self):
        input_filename = self.extracted_data
        output_filename = self.transformed_data
        transform(input_filename, output_filename)

    def test_load(self):
        input_filename = self.transformed_data
        self.validate_load(self.config, input_filename)