import os
import sys
import pandas
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import ibge  # noqa: E402
from mock_helpers import mock_json, get_sample_json  # noqa: E402


class TestIBGESearch(unittest.TestCase):
    def setUp(self):
        mock_json(
            path="seriesbr.ibge.get_json", json=get_sample_json("ibge_search_results.json")
        ).start()

    def test_search_json_parser(self):
        df = ibge.search()
        self.assertIsInstance(df, pandas.DataFrame)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
