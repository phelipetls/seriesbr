import os
import sys
import unittest
import pandas as pd

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mock_helpers import get_json  # noqa: E402
from seriesbr.helpers.response import (
    bcb_json_to_df,
    ipea_json_to_df,
    ibge_json_to_df,
)  # noqa: E402


def mocked_get_json(json):
    return json


@patch("seriesbr.helpers.response.get_json", mocked_get_json)
class TestJsonParsers(unittest.TestCase):
    """Test getting a timeseries in JSON format and parsing it into a dataframe"""

    def test_bcb_parser(self):
        df = bcb_json_to_df(get_json("bcb_json.json"), 11, "Selic")
        self.assertIsInstance(df, pd.DataFrame)

    def test_ipea_parser(self):
        df = ipea_json_to_df(get_json("ipea_json.json"), "Código", "Nome")
        self.assertIsInstance(df, pd.DataFrame)

    def test_ibge_parser(self):
        df = ibge_json_to_df(get_json("ibge_json.json"))
        self.assertIsInstance(df, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
