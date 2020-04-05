import os
import sys
import pandas
import unittest

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import ibge  # noqa: E402
from mock_helpers import mock_json, get_sample_json  # noqa: E402


class TestIBGESearch(unittest.TestCase):
    """Test if IBGE parses IBGE's API JSON response correctly"""

    def setUp(self):
        mock_json(
            path="seriesbr.ibge.get_json", json=get_sample_json("ibge_search_results.json")
        ).start()

    def test_search_json_parser(self):
        df = ibge.search()
        self.assertIsInstance(df, pandas.DataFrame)

    def test_if_ibge_search_results_dataframe_is_empty(self):
        df = ibge.search()
        self.assertFalse(df.empty)

    def tearDown(self):
        patch.stopall()


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
