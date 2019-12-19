import os
import sys
import unittest
import datetime

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ipea


def mocked_json_to_df(url, code, name):
    return url


def mocked_today_date():
    return datetime.datetime(2019, 12, 2)


def mocked_get_metadata(code):
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"Metadados('{code}')"
    url = f"{baseurl}{resource_path}"
    return url


def mocked_list_metadata(resource_path):
    baseurl = "http://www.ipeadata.gov.br/api/odata4/"
    url = f"{baseurl}{resource_path}"
    return url


@patch('seriesbr.ipea.ipea_json_to_df', mocked_json_to_df)
@patch('seriesbr.ipea.get_metadata', mocked_get_metadata)
@patch('seriesbr.ipea.list_metadata_helper', mocked_list_metadata)
@patch('seriesbr.helpers.dates.today_date', mocked_today_date)
class IPEAtest(unittest.TestCase):

    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='BM12_CRLIN12')?$select=VALDATA,VALVALOR"

    maxDiff = None

    def test_url_no_dates(self):
        correct = self.baseurl + "&$filter=VALDATA ge 1900-01-01T00:00:00-00:00 and VALDATA le 2019-12-02T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12"), correct)

    ## Test only with start dates

    def test_url_start_dates_complete_dates(self):
        correct = self.baseurl + "&$filter=VALDATA ge 2019-02-01T00:00:00-00:00 and VALDATA le 2019-12-02T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="01-02-2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="01/02/2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="01022019"), correct)

    def test_url_start_dates_month_year(self):
        correct = self.baseurl + "&$filter=VALDATA ge 2019-02-01T00:00:00-00:00 and VALDATA le 2019-12-02T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="02-2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="02/2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="022019"), correct)

    def test_url_start_dates_year_only(self):
        correct = self.baseurl + "&$filter=VALDATA ge 2019-01-01T00:00:00-00:00 and VALDATA le 2019-12-02T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="2019"), correct)

    ## Test only with end dates

    def test_url_end_dates_complete_dates(self):
        correct = self.baseurl + "&$filter=VALDATA ge 1900-01-01T00:00:00-00:00 and VALDATA le 2019-02-01T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="01-02-2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="01/02/2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="01022019"), correct)

    def test_url_end_dates_month_year(self):
        correct = self.baseurl + "&$filter=VALDATA ge 1900-01-01T00:00:00-00:00 and VALDATA le 2019-02-28T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="02-2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="02/2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="022019"), correct)

    def test_url_end_dates_year_only(self):
        correct = self.baseurl + "&$filter=VALDATA ge 1900-01-01T00:00:00-00:00 and VALDATA le 2019-12-31T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", end="2019"), correct)

    ## Test with both start and end dates

    def test_url_start_and_end_dates_complete_dates(self):
        correct = self.baseurl + "&$filter=VALDATA ge 2016-05-04T00:00:00-00:00 and VALDATA le 2019-02-01T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="04/05/2016", end="01/02/2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="04-05-2016", end="01-02-2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="04052016", end="01022019"), correct)

    def test_url_start_and_end_dates_month_year(self):
        correct = self.baseurl + "&$filter=VALDATA ge 2016-05-01T00:00:00-00:00 and VALDATA le 2019-02-28T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="05/2016", end="02/2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="05-2016", end="02-2019"), correct)
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="052016", end="022019"), correct)

    def test_url_start_and_end_dates_year_only(self):
        correct = self.baseurl + "&$filter=VALDATA ge 2016-01-01T00:00:00-00:00 and VALDATA le 2019-12-31T00:00:00-00:00"
        self.assertEqual(ipea.get_serie("BM12_CRLIN12", start="2016", end="2019"), correct)

    ## Test metadata function

    def test_get_metadata(self):
        self.assertEqual(ipea.get_metadata("BM12_CRLIN12"), "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('BM12_CRLIN12')")

    def test_list_countries(self):
        self.assertEqual(ipea.list_countries(), "http://www.ipeadata.gov.br/api/odata4/Paises")

    def test_list_themes(self):
        self.assertEqual(ipea.list_themes(), "http://www.ipeadata.gov.br/api/odata4/Temas")


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
