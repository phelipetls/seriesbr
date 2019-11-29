import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import bcb
from seriesbr import ipea
from pandas import api


class TestTypes(unittest.TestCase):

    def test_bcb_dataframe_dtypes(self):
        df = bcb.get_serie(20786)
        self.assertTrue(api.types.is_datetime64_any_dtype(df.index))
        self.assertTrue(api.types.is_float_dtype(df.iloc[:, 0]))

    def test_ipea_dataframe_dtypes(self):
        df = ipea.get_serie("BM12_CRLIN12")
        self.assertTrue(api.types.is_datetime64_any_dtype(df.index))
        self.assertTrue(api.types.is_float_dtype(df.iloc[:, 0]))


if __name__ == "__main__":
    unittest.main()
