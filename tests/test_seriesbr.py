import unittest
import pandas as pd

from seriesbr import seriesbr
from unittest.mock import patch
from mock_helpers import get_sample_json


def generate_jsons():
    """Simulate making a IPEA API response, then a BCB API response"""
    srcs = ["ipea", "bcb"]
    for src in srcs:
        yield get_sample_json(src + "_json.json")


class TestSeriesBr(unittest.TestCase):
    """Test getting IPEA and BCB series at once"""

    @classmethod
    @patch("seriesbr.helpers.timeseries.get_json")
    def setUpClass(cls, g):
        g.side_effect = generate_jsons()

        cls.df = seriesbr.get_series(
            {"Inadimplência": "BM12_CRLIN12", "Spread": 20786}, start="2015", end="2015"
        )

    def test_if_data_frame_is_empty(self):
        self.assertFalse(self.df.empty)

    def test_data_frame_columns(self):
        test = self.df.columns.tolist()
        expected = ["Inadimplência", "Spread"]
        self.assertListEqual(test, expected)

    def test_data_frame_columns_dtypes(self):
        test = [pd.api.types.is_float(dtype) for dtype in self.df.dtypes]
        expected = [True, True]
        self.assertLessEqual(test, expected)

    def test_data_frame_index_dtype(self):
        test = self.df.index
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(test))


if __name__ == "__main__":
    unittest.main()
