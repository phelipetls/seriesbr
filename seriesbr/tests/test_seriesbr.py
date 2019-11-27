import os
import sys
import unittest
import pandas

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from seriesbr import seriesbr


class SERIESBRtest(unittest.TestCase):

    df = seriesbr.get_series({"Spread": 20786, "Selic": 4189, "PIB_mensal": 4380})

    def test_get_series_returns_data_frame(self):
        self.assertIsInstance(self.df, pandas.DataFrame)

    def test_if_names_of_columns_are_right(self):
        self.assertListEqual(self.df.columns.to_list(), ["Spread", "Selic", "PIB_mensal"])


if __name__ == "__main__":
    unittest.main()
