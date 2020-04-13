import unittest
import datetime
import pandas as pd

from seriesbr import bcb
from unittest.mock import patch
from mock_helpers import get_sample_json
from seriesbr.helpers.response import bcb_json_to_df


@patch("seriesbr.helpers.response.get_json", return_value=get_sample_json("bcb_json.json"))
class TestBcbJsonParser(unittest.TestCase):

    def test_parser(self, _):
        df = bcb_json_to_df("https://api.call", 11, "Selic")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(pd.api.types.is_datetime64_dtype(df.index))
        self.assertTrue(pd.api.types.is_float_dtype(df.values))


def mocked_get_today_date():
    """Use this date as if it were today"""
    return datetime.datetime(2019, 12, 2)


@patch("seriesbr.helpers.dates.get_today_date", mocked_get_today_date)
class TestBcbUrl(unittest.TestCase):
    """Test Bcb url builder to get a time series"""

    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?format=json"

    def test_url_no_dates(self):
        test = bcb.build_url(11)
        expected = f"{self.url}&dataInicial=01/01/1900&dataFinal=02/12/2019"
        self.assertEqual(test, expected)

    def test_url_start_date_year_only(self):
        test = bcb.build_url(11, start="2013")
        expected = f"{self.url}&dataInicial=01/01/2013&dataFinal=02/12/2019"
        self.assertEqual(test, expected)

    def test_url_start_date_month_and_year(self):
        test = bcb.build_url(11, start="07-2013")
        expected = f"{self.url}&dataInicial=01/07/2013&dataFinal=02/12/2019"
        self.assertEqual(test, expected)

    def test_url_end_date_year_only(self):
        test = bcb.build_url(11, end="1990")
        expected = f"{self.url}&dataInicial=01/01/1900&dataFinal=31/12/1990"
        self.assertEqual(test, expected)

    def test_url_end_date_month_and_year(self):
        test = bcb.build_url(11, end="06-1990")
        expected = f"{self.url}&dataInicial=01/01/1900&dataFinal=30/06/1990"
        self.assertEqual(test, expected)

    def test_url_end_date_full(self):
        test = bcb.build_url(11, end="05032016")
        expected = f"{self.url}&dataInicial=01/01/1900&dataFinal=05/03/2016"
        self.assertEqual(test, expected)

    def test_url_start_and_end_date_year_only(self):
        test = bcb.build_url(11, start="2013", end="09/2014")
        expected = f"{self.url}&dataInicial=01/01/2013&dataFinal=30/09/2014"
        self.assertEqual(test, expected)

    def test_url_start_and_end_date_month_and_year(self):
        test = bcb.build_url(11, start="07-2013", end="09-2014")
        expected = f"{self.url}&dataInicial=01/07/2013&dataFinal=30/09/2014"
        self.assertEqual(test, expected)

    def test_url_start_and_end_date_full_dates(self):
        test = bcb.build_url(11, start="05032016", end="25102017")
        expected = f"{self.url}&dataInicial=05/03/2016&dataFinal=25/10/2017"
        self.assertEqual(test, expected)

    def test_url_last_n(self):
        test = bcb.build_url(11, last_n=30)
        expected = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/30?format=json"
        self.assertEqual(test, expected)

    def test_invalid_code(self):
        with self.assertRaises(AssertionError):
            bcb.build_url({})

    def test_crazy_date(self):
        with self.assertRaises(ValueError):
            bcb.build_url(11, start="asfhajksfsa")


class TestBcbGetMetadata(unittest.TestCase):
    """Test BCB get_metadata function parser and URL builder"""

    def test_url(self):
        test = bcb.build_metadata_url(20786)

        url = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
        expected = url + "fq=codigo_sgs:20786"

        self.assertEqual(test, expected)

    @patch(
        "seriesbr.helpers.metadata.get_json",
        return_value=get_sample_json("bcb_metadata.json"),
    )
    def test_dataframe(self, _):
        df = bcb.get_metadata(20786)
        self.assertFalse(df.empty)


class TestBCBSearch(unittest.TestCase):
    """Test if BCB search functions parsers and URL builders"""

    url = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"

    def test_search_bcb(self):
        test = bcb.build_search_url("spread")
        expected = f"{self.url}q=spread&rows=10&start=1&sort=score desc"
        self.assertEqual(test, expected)

    def test_search_multiple_strings(self):
        test = bcb.build_search_url("spread", "mensal", "livre")
        expected = f"{self.url}q=spread&rows=10&start=1&sort=score desc&fq=mensal+livre"
        self.assertEqual(test, expected)

    def test_search_with_pagination(self):
        test = bcb.build_search_url("spread", "mensal", "livre", rows=30, start=5)
        expected = f"{self.url}q=spread&rows=30&start=5&sort=score desc&fq=mensal+livre"
        self.assertEqual(test, expected)

    @patch(
        "seriesbr.helpers.searching.get_json",
        return_value=get_sample_json("bcb_search_results.json"),
    )
    def test_bcb_get_search_results(self, _):
        df = bcb.bcb_get_search_results("https://fake.com?json=call")

        test = df.columns.tolist()
        expected = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]

        self.assertListEqual(test, expected)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
