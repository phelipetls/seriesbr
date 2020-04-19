import unittest
import pandas as pd

from seriesbr import ipea
from unittest.mock import patch
from seriesbr.helpers import api
from mock_helpers import get_sample_json

settings = {"return_value": get_sample_json("ipea_json.json")}


@patch("seriesbr.helpers.timeseries.get_json", **settings)
class TestIpeaJsonParser(unittest.TestCase):
    """Test conversion of IPEA timeseries json into DataFrame"""

    def test_timeseries_json_to_dataframe(self, _):
        df = ipea.get_series({"Selic": "BM12_CRLIN12"})

        self.assertIsInstance(df, pd.DataFrame)

        self.assertTrue(pd.api.types.is_datetime64_dtype(df.index))
        self.assertTrue(pd.api.types.is_float_dtype(df.values))

        self.assertListEqual(df.columns.tolist(), ["Selic"])


settings = {"return_value": get_sample_json("ipea_metadata.json")}


class TestIpeaGetMetadata(unittest.TestCase):
    """Test IPEA get_metadata function parser and URL builder"""

    def test_url(self):
        url = ipea.build_metadata_url("BM12_CRLIN12")
        expected_url = (
            "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('BM12_CRLIN12')"
        )
        self.assertEqual(url, expected_url)

    @patch("seriesbr.helpers.metadata.get_json", **settings)
    def test_dataframe(self, _):
        df = ipea.get_metadata(21789)
        self.assertFalse(df.empty)


settings = {"return_value": get_sample_json("ipea_search_results.json")}


class TestIpeaSearch(unittest.TestCase):
    """Test Ipea search functions"""

    @patch("seriesbr.helpers.search_results.get_json", **settings)
    def test_dataframe(self, _):
        df = ipea.search("Selic")
        self.assertFalse(df.empty)

    def test_ipea_select(self):
        test = api.ipea_select()
        expected = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"
        self.assertEqual(test, expected)

    def test_ipea_select_default_field(self):
        test = api.ipea_select(["PERNOME"])
        expected = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"
        self.assertEqual(test, expected)

    def test_ipea_select_additional_field(self):
        test = api.ipea_select(["FNTNOME"])
        expected = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,FNTNOME"
        self.assertEqual(test, expected)

    def test_ipea_filter_simple(self):
        test = api.ipea_filter("SELIC")
        expected = "&$filter=contains(SERNOME,'SELIC')"
        self.assertEqual(test, expected)

    def test_ipea_filter_contains_operator(self):
        test = api.ipea_filter("SELIC", {"PERNOME": ["mensal", "trimestral"]})
        expected = (
            "&$filter=contains(SERNOME,'SELIC') and"
            " (contains(PERNOME,'mensal') or contains(PERNOME,'trimestral'))"
        )
        self.assertEqual(test, expected)

    def test_ipea_filter_equal_operator(self):
        test = api.ipea_filter("SELIC", {"SERSTATUS": ["A", "I"], "SERNUMERICA": 1})
        expected = (
            "&$filter=contains(SERNOME,'SELIC') and"
            " (SERSTATUS eq 'A' or SERSTATUS eq 'I') and"
            " SERNUMERICA eq 1"
        )
        self.assertEqual(test, expected)


@patch("seriesbr.helpers.lists.get_json")
class TestIpeaListFunctions(unittest.TestCase):
    """Test Ipea list functions dataframe converters"""

    def test_list_themes(self, m):
        m.return_value = get_sample_json("ipea_temas.json")

        columns = ipea.list_themes().columns.tolist()
        expected_columns = ["TEMCODIGO", "TEMCODIGO_PAI", "TEMNOME"]

        self.assertListEqual(columns, expected_columns)

    def test_list_countries(self, m):
        m.return_value = get_sample_json("ipea_paises.json")

        columns = ipea.list_countries().columns.tolist()
        expected_columns = ["PAICODIGO", "PAINOME"]

        self.assertListEqual(columns, expected_columns)

    def test_list_metadata(self, _):
        df = ipea.list_metadata()
        self.assertFalse(df.empty)


if __name__ == "__main__":
    unittest.main(failfast=True)
