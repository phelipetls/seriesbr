import os
import sys
import json
import pandas
import unittest

from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr.helpers.response import json_to_dataframe, ibge_json_to_dataframe


class TestBCBJsonParser(unittest.TestCase):

    def setUp(self):
        json_path = Path(__file__).resolve().parent / "sample_jsons" / "bcb_json"
        with json_path.open() as json_file:
            sample_json = json.load(json_file)
        self.df = json_to_dataframe(sample_json, 11, "Selic", "data", "valor", "%d/%m/%Y")

    def test_if_returns_data_frame(self):
        self.assertIsInstance(self.df, pandas.DataFrame)

    def test_index_dtype(self):
        self.assertTrue(pandas.api.types.is_datetime64_dtype(self.df.index))


class TestIPEAJsonParser(unittest.TestCase):

    def setUp(self):
        json_path = Path(__file__).resolve().parent / "sample_jsons" / "ipea_json"
        with json_path.open() as json_file:
            sample_json = json.load(json_file)
        self.df = json_to_dataframe(sample_json["value"], "Código", "Nome", "VALDATA", "VALVALOR", "%Y-%m-%dT%H:%M:%S")

    def test_if_returns_data_frame(self):
        self.assertIsInstance(self.df, pandas.DataFrame)

    def test_index_dtype(self):
        self.assertTrue(pandas.api.types.is_datetime64_dtype(self.df.index))


class TestIBGEJsonParser(unittest.TestCase):

    def setUp(self):
        json_path = Path(__file__).resolve().parent / "sample_jsons" / "ibge_json"
        with json_path.open() as json_file:
            sample_json = json.load(json_file)
        self.df = ibge_json_to_dataframe(sample_json)

    def test_if_returns_data_frame(self):
        self.assertIsInstance(self.df, pandas.DataFrame)

    def test_index_dtype(self):
        self.assertTrue(pandas.api.types.is_datetime64_dtype(self.df.index))


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
