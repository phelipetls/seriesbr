import os
import sys
import unittest
import pandas

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from seriesbr import ipea


class IPEAtest(unittest.TestCase):

    series = {
        "IGP": "PAN12_IGPDIG12",
        "INAD": "BM12_CRLIN12",
        "IBC": "SGS12_IBCBRDESSAZ12",
    }

    df = ipea.get_series(series)

    def test_if_get_series_returns_data_frame(self):
        self.assertIsInstance(self.df, pandas.DataFrame)

    def test_if_search_empty_string_returns_data_frame(self):
        self.assertIsInstance(ipea.search(""), pandas.DataFrame)

    def test_column_names(self):
        self.assertListEqual(self.df.columns.to_list(), ["IGP", "INAD", "IBC"])

    def test_search_with_multiple_filters(self):
        result = ipea.search(BASNOME="Macroeconômico", PERNOME="Mensal", UNINOME="(p.p.)")
        self.assertGreater(len(result), 0)

    def test_if_metadata_returns_dict(self):
        self.assertIsInstance(ipea.get_metadata("PAN12_IGPDIG12"), dict)


if __name__ == "__main__":
    unittest.main()
