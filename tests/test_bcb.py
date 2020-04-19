import unittest
import pandas as pd

from seriesbr import bcb
from unittest.mock import patch
from mock_helpers import get_sample_json

settings = {"return_value": get_sample_json("bcb_json.json")}


@patch("seriesbr.helpers.timeseries.get_json", **settings)
class TestBcbJsonParser(unittest.TestCase):
    """Test conversion of BCB timeseries json into DataFrame"""

    def test_timeseries_json_to_dataframe(self, _):
        df = bcb.get_series({"Selic": 11})

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(pd.api.types.is_datetime64_dtype(df.index))
        self.assertTrue(pd.api.types.is_float_dtype(df.values))
        self.assertListEqual(df.columns.tolist(), ["Selic"])


settings = {"return_value": get_sample_json("bcb_metadata.json")}


class TestBcbGetMetadata(unittest.TestCase):
    """Test BCB get_metadata function parser and URL builder"""

    def test_url(self):
        url = bcb.build_metadata_url(20786)

        expected_url = (
            "https://dadosabertos.bcb.gov.br/api/3/action/"
            "package_search?fq=codigo_sgs:20786"
        )

        self.assertEqual(url, expected_url)

    @patch("seriesbr.helpers.metadata.get_json", **settings)
    def test_dataframe(self, _):
        df = bcb.get_metadata(20786)

        self.assertFalse(df.empty)


settings = {"return_value": get_sample_json("bcb_search_results.json")}


class TestBCBSearch(unittest.TestCase):
    """Test BCB search functions parsers and URL builders"""

    url = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"

    def test_search_bcb(self):
        url = bcb.build_search_url("spread")
        expected_url = "q=spread&rows=10&start=1&sort=score desc"

        self.assertEqual(url, f"{self.url}{expected_url}")

    def test_search_multiple_strings(self):
        url = bcb.build_search_url("spread", "mensal", "livre")
        expected_url = "q=spread&rows=10&start=1&sort=score desc&fq=mensal+livre"

        self.assertEqual(url, f"{self.url}{expected_url}")

    def test_search_with_pagination(self):
        url = bcb.build_search_url("spread", "mensal", "livre", rows=30, start=5)
        expected_url = "q=spread&rows=30&start=5&sort=score desc&fq=mensal+livre"

        self.assertEqual(url, f"{self.url}{expected_url}")

    @patch("seriesbr.helpers.search_results.get_json", **settings)
    def test_bcb_get_search_results(self, _):
        df = bcb.search("Selic")

        columns = df.columns.tolist()
        expected_columns = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]

        self.assertListEqual(columns, expected_columns)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
