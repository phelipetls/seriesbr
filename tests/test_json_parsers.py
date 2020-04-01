import os
import sys
import unittest
import pandas as pd

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mock_helpers import get_sample_json  # noqa: E402
from seriesbr.helpers.response import (
    bcb_json_to_df,
    ipea_json_to_df,
    ibge_json_to_df,
)  # noqa: E402


def mocked_get_json(json):
    return json


@patch("seriesbr.helpers.response.get_json", mocked_get_json)
class TestJsonParsers(unittest.TestCase):
    """Test getting a timeseries in JSON format and parsing it into a DataFrame"""

    def test_bcb_parser(self):
        df = bcb_json_to_df(get_sample_json("bcb_json.json"), 11, "Selic")
        # assert it is a DataFrame
        self.assertIsInstance(df, pd.DataFrame)
        # index is datetime
        self.assertTrue(pd.api.types.is_datetime64_dtype(df.index))
        # series is float
        self.assertTrue(pd.api.types.is_float_dtype(df.values))

    def test_ipea_parser(self):
        df = ipea_json_to_df(get_sample_json("ipea_json.json"), "Código", "Nome")
        # assert it is a DataFrame
        self.assertIsInstance(df, pd.DataFrame)
        # index is datetime
        self.assertTrue(pd.api.types.is_datetime64_dtype(df.index))
        # series is float
        self.assertTrue(pd.api.types.is_float_dtype(df.values))

    def test_ibge_parser(self):
        df = ibge_json_to_df(get_sample_json("ibge_json.json"))
        # assert it is a DataFrame
        self.assertIsInstance(df, pd.DataFrame)
        # index is datetime
        self.assertTrue(pd.api.types.is_datetime64_dtype(df.index))


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
