import os
import sys
import json
import pandas
import unittest
from unittest.mock import patch

from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr.helpers.response import bcb_json_to_df, ipea_json_to_df, ibge_json_to_df


def mocked_get_json(url):
    return url


class TestBCBJsonParser(unittest.TestCase):

    @patch('seriesbr.helpers.response.get_json', mocked_get_json)
    def setUp(self):
        json_path = Path(__file__).resolve().parent / "sample_jsons" / "bcb_json"
        with json_path.open() as json_file:
            sample_json = json.load(json_file)
        self.df = bcb_json_to_df(sample_json, 11, "Selic")

    def test_if_returns_data_frame(self):
        self.assertIsInstance(self.df, pandas.DataFrame)

    def test_index_dtype(self):
        self.assertTrue(pandas.api.types.is_datetime64_dtype(self.df.index))


class TestIPEAJsonParser(unittest.TestCase):

    @patch('seriesbr.helpers.response.get_json', mocked_get_json)
    def setUp(self):
        json_path = Path(__file__).resolve().parent / "sample_jsons" / "ipea_json"
        with json_path.open() as json_file:
            sample_json = json.load(json_file)
        self.df = ipea_json_to_df(sample_json, "Código", "Nome")

    def test_if_returns_data_frame(self):
        self.assertIsInstance(self.df, pandas.DataFrame)

    def test_index_dtype(self):
        self.assertTrue(pandas.api.types.is_datetime64_dtype(self.df.index))


class TestIBGEJsonParser(unittest.TestCase):

    @patch('seriesbr.helpers.response.get_json', mocked_get_json)
    def setUp(self):
        json_path = Path(__file__).resolve().parent / "sample_jsons" / "ibge_json"
        with json_path.open() as json_file:
            sample_json = json.load(json_file)
        self.df = ibge_json_to_df(sample_json)

    def test_if_returns_data_frame(self):
        self.assertIsInstance(self.df, pandas.DataFrame)

    def test_index_dtype(self):
        self.assertTrue(pandas.api.types.is_datetime64_dtype(self.df.index))


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
