import os
import sys
import unittest
import pandas as pd

from dummy_dag_helper_functions import change_data_types
from test_base import Test

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class MyTest(Test):
    def setUp(self):
        self.working_dir =  os.path.dirname(__file__)
        self.config = os.path.join(
            self.working_dir, "dummy_dag.yml"
        )

    def test_config_is_valid(self):
        self.validate_config(self.config)

    def test_change_data_type(self):
        df = pd.DataFrame({
            'Rk': ['1', '2', '3', '4'],
            'Age': ['25', '28', '22', '30']
        })

        df = change_data_types(df)

        assert (df['Rk'].dtype, df['Age'].dtype) == ('int','int')
        