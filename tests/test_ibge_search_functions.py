import os
import sys
import json
import pandas
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ibge


def mocked_get_json(url):
    json_path = Path(__file__).resolve().parent / "sample_jsons" / "ibge_search_input"
    with json_path.open() as search_input:
        return json.load(search_input)


class TestIBGESearch(unittest.TestCase):

    @patch('seriesbr.ibge.get_json', mocked_get_json)
    def setUp(self):
        self.df = ibge.search()

    def test_search_json_parser(self):
        self.assertIsInstance(self.df, pandas.DataFrame)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
