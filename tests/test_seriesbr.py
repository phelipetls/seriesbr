import os
import sys
import unittest
import pandas as pd

from unittest.mock import patch
from mock_helpers import mock_json, get_sample_json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import seriesbr  # noqa: E402


def generate_jsons():
    """Simulate making a IPEA API response, then a BCB API response"""
    srcs = ["ipea", "bcb"]
    for src in srcs:
        yield get_sample_json(src + "_json.json")


class TestSeriesBr(unittest.TestCase):
    """Test getting IPEA and BCB series at once"""

    @classmethod
    @patch("seriesbr.helpers.response.get_json")
    def setUpClass(cls, mocked_get_json):
        mocked_get_json.side_effect = generate_jsons()

        cls.df = seriesbr.get_series("BM12_CRLIN12", 20786, start="2015", end="2015")

    def test_if_data_frame_is_empty(self):
        self.assertFalse(self.df.empty)

    def test_data_frame_columns(self):
        test = self.df.columns.tolist()
        expected = ["BM12_CRLIN12", 20786]
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
