import os
import sys
import unittest
import pandas

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from seriesbr import bcb


class BCBtest(unittest.TestCase):

    df = bcb.get_series({"Spread": 20786, "Selic": 4189, "PIB_mensal": 4380})

    def test_if_get_series_returns_data_frame(self):
        self.assertIsInstance(self.df, pandas.DataFrame)

    def test_if_search_empty_string_returns_data_frame(self):
        self.assertIsInstance(bcb.search(""), pandas.DataFrame)

    def test_if_search_returns_data_frame(self):
        self.assertIsInstance(bcb.search("Spread"), pandas.DataFrame)

    def test_if_search_two_params_returns_data_frame(self):
        self.assertIsInstance(bcb.search("Spread", "Mensal"), pandas.DataFrame)

    def test_if_search_three_params_returns_data_frame(self):
        self.assertIsInstance(bcb.search("Spread", "Pontos percentuais", "Mensal"), pandas.DataFrame)

    def test_if_columns_are_keys(self):
        self.assertListEqual(self.df.columns.to_list(), ["Spread", "Selic", "PIB_mensal"])

    def test_if_get_metadata_works(self):
        self.assertIsInstance(bcb.get_metadata(20786), dict)


if __name__ == "__main__":
    unittest.main()