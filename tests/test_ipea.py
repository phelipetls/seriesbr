import os
import sys
import unittest
import datetime
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ipea


def mocked_parse_response(url, code, name):
    return url


def mocked_today_date():
    return datetime.datetime(2019, 12, 2)


def mocked_search_results(url):
    return url


def mocked_utc_offset():
    return "-03:00"


def mocked_get_metadata(cod):
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"Metadados('{cod}')"
    url = f"{baseurl}{resource_path}"
    return url


def mocked_list_metadata(resource_path):
    baseurl = "http://www.ipeadata.gov.br/api/odata4/"
    url = f"{baseurl}{resource_path}"
    return url


def mocked_ipea_search_only_filter(SERNOME="", **fields):
    filter_query = ipea.ipea_make_filter_query(SERNOME, fields)
    return filter_query


@patch('seriesbr.ipea.parse_ipea_response', mocked_parse_response)
@patch('seriesbr.ipea.get_metadata', mocked_get_metadata)
@patch('seriesbr.ipea.list_metadata', mocked_list_metadata)
@patch('seriesbr.helpers.dates.today_date', mocked_today_date)
@patch('seriesbr.helpers.dates.get_utc_offset', mocked_utc_offset)
class IPEAtest(unittest.TestCase):

    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='BM12_CRLIN12')?$select=VALDATA,VALVALOR"

    maxDiff = None

    def test_url_no_dates(self):
        truth = self.baseurl + "&$filter=VALDATA ge 1900-01-01T00:00:00-03:00 and VALDATA le 2019-12-02T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12"), truth)

    ## Test only with start dates

    def test_url_start_dates_complete_dates(self):
        truth = self.baseurl + "&$filter=VALDATA ge 2019-02-01T00:00:00-03:00 and VALDATA le 2019-12-02T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="01-02-2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="01/02/2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="01022019"), truth)

    def test_url_start_dates_month_year(self):
        truth = self.baseurl + "&$filter=VALDATA ge 2019-02-01T00:00:00-03:00 and VALDATA le 2019-12-02T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="02-2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="02/2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="022019"), truth)

    def test_url_start_dates_year_only(self):
        truth = self.baseurl + "&$filter=VALDATA ge 2019-01-01T00:00:00-03:00 and VALDATA le 2019-12-02T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="2019"), truth)

    ## Test only with end dates

    def test_url_end_dates_complete_dates(self):
        truth = self.baseurl + "&$filter=VALDATA ge 1900-01-01T00:00:00-03:00 and VALDATA le 2019-02-01T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="01-02-2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="01/02/2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="01022019"), truth)

    def test_url_end_dates_month_year(self):
        truth = self.baseurl + "&$filter=VALDATA ge 1900-01-01T00:00:00-03:00 and VALDATA le 2019-02-28T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="02-2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="02/2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="022019"), truth)

    def test_url_end_dates_year_only(self):
        truth = self.baseurl + "&$filter=VALDATA ge 1900-01-01T00:00:00-03:00 and VALDATA le 2019-12-31T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="2019"), truth)

    ## Test with both start and end dates

    def test_url_start_and_end_dates_complete_dates(self):
        truth = self.baseurl + "&$filter=VALDATA ge 2016-05-04T00:00:00-03:00 and VALDATA le 2019-02-01T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="04/05/2016", end="01/02/2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="04-05-2016", end="01-02-2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="04052016", end="01022019"), truth)

    def test_url_start_and_end_dates_month_year(self):
        truth = self.baseurl + "&$filter=VALDATA ge 2016-05-01T00:00:00-03:00 and VALDATA le 2019-02-28T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="05/2016", end="02/2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="05-2016", end="02-2019"), truth)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="052016", end="022019"), truth)

    def test_url_start_and_end_dates_year_only(self):
        truth = self.baseurl + "&$filter=VALDATA ge 2016-01-01T00:00:00-03:00 and VALDATA le 2019-12-31T00:00:00-03:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="2016", end="2019"), truth)

    ## Test metadata function

    @patch('seriesbr.ipea.get_metadata', mocked_get_metadata)
    def test_get_metadata(self):
        self.assertEqual(ipea.get_metadata("BM12_CRLIN12"), "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('BM12_CRLIN12')")

    def test_list_countries(self):
        self.assertEqual(ipea.list_countries(), "http://www.ipeadata.gov.br/api/odata4/Paises")

    def test_list_themes(self):
        self.assertEqual(ipea.list_themes(), "http://www.ipeadata.gov.br/api/odata4/Temas")

    @patch('seriesbr.ipea.search', mocked_ipea_search_only_filter)
    def test_search_filters(self):
        self.assertEqual(ipea.search(SERNOME="Spread"), "&$filter=contains(SERNOME,'Spread')")
        self.assertEqual(ipea.search(SERNOME="Spread", TEMCODIGO=12), "&$filter=contains(SERNOME,'Spread') and TEMCODIGO eq 12")
        self.assertEqual(ipea.search(SERNOME="Spread", TEMCODIGO=12, FNTNOME="IBGE"), "&$filter=contains(SERNOME,'Spread') and TEMCODIGO eq 12 and contains(FNTNOME,'IBGE')")
        self.assertEqual(ipea.search(TEMCODIGO=12, FNTNOME="IBGE"), "&$filter=TEMCODIGO eq 12 and contains(FNTNOME,'IBGE')")
        self.assertEqual(ipea.search(TEMCODIGO=12, FNTNOME="IBGE", SERNUMERICA=1), "&$filter=TEMCODIGO eq 12 and contains(FNTNOME,'IBGE') and SERNUMERICA eq 1")
        self.assertEqual(ipea.search(SERNOME="Selic", TEMCODIGO=12, FNTNOME="IBGE", SERNUMERICA=1), "&$filter=contains(SERNOME,'Selic') and TEMCODIGO eq 12 and contains(FNTNOME,'IBGE') and SERNUMERICA eq 1")


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
