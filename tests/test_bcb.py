import os
import sys
import unittest
import datetime
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import bcb


def mocked_parse_response(url, code, name):
    return url


def mocked_today_date():
    return datetime.datetime(2019, 12, 2)


def mocked_search_results(url):
    return url


@patch('seriesbr.bcb.parse_bcb_response', mocked_parse_response)
@patch('seriesbr.helpers.dates.today_date', mocked_today_date)
class BCBtest(unittest.TestCase):

    baseurl = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?format=json"

    def test_url_no_dates(self):
        correct = self.baseurl + "&dataInicial=01/01/1900&dataFinal=02/12/2019"
        self.assertEqual(bcb.get_serie(11), correct)

    ## Testing start dates argument

    def test_url_start_date_year_only(self):
        correct = self.baseurl + "&dataInicial=01/01/2013&dataFinal=02/12/2019"
        self.assertEqual(bcb.get_serie(11, start="2013"), correct)

    def test_url_start_date_month_and_year(self):
        correct = self.baseurl + "&dataInicial=01/07/2013&dataFinal=02/12/2019"
        self.assertEqual(bcb.get_serie(11, start="07-2013"), correct)
        self.assertEqual(bcb.get_serie(11, start="07/2013"), correct)
        self.assertEqual(bcb.get_serie(11, start="072013"), correct)

    def test_url_start_date_month_and_year(self):
        correct = self.baseurl + "&dataInicial=01/07/2013&dataFinal=02/12/2019"
        self.assertEqual(bcb.get_serie(11, start="01-07-2013"), correct)
        self.assertEqual(bcb.get_serie(11, start="01/07/2013"), correct)
        self.assertEqual(bcb.get_serie(11, start="01072013"), correct)

    ## Testing end dates argument

    def test_url_end_date_year_only(self):
        correct = self.baseurl + "&dataInicial=01/01/1900&dataFinal=31/12/1990"
        self.assertEqual(bcb.get_serie(11, end="1990"), correct)

    def test_url_end_date_month_and_year(self):
        correct = self.baseurl + "&dataInicial=01/01/1900&dataFinal=30/06/1990"
        self.assertEqual(bcb.get_serie(11, end="06/1990"), correct)
        self.assertEqual(bcb.get_serie(11, end="06-1990"), correct)
        self.assertEqual(bcb.get_serie(11, end="061990"), correct)

    def test_url_complete_dates(self):
        correct = self.baseurl + "&dataInicial=01/01/1900&dataFinal=05/03/2016"
        self.assertEqual(bcb.get_serie(11, end="05/03/2016"), correct)
        self.assertEqual(bcb.get_serie(11, end="05-03-2016"), correct)
        self.assertEqual(bcb.get_serie(11, end="05032016"), correct)

    ## Testing start and end dates arguments

    def test_url_start_and_end_date_year_only(self):
        correct = self.baseurl + "&dataInicial=01/01/2013&dataFinal=30/09/2014"
        self.assertEqual(bcb.get_serie(11, start="2013", end="09/2014"), correct)
        self.assertEqual(bcb.get_serie(11, start="2013", end="09-2014"), correct)
        self.assertEqual(bcb.get_serie(11, start="2013", end="092014"), correct)

    def test_url_start_and_end_date_month_and_year(self):
        correct = self.baseurl + "&dataInicial=01/07/2013&dataFinal=30/09/2014"
        self.assertEqual(bcb.get_serie(11, start="07/2013", end="09/2014"), correct)
        self.assertEqual(bcb.get_serie(11, start="07-2013", end="09-2014"), correct)
        self.assertEqual(bcb.get_serie(11, start="072013", end="092014"), correct)

    def test_url_start_and_end_date_complete_dates(self):
        correct = self.baseurl + "&dataInicial=05/03/2016&dataFinal=25/10/2017"
        self.assertEqual(bcb.get_serie(11, start="05/03/2016", end="25/10/2017"), correct)
        self.assertEqual(bcb.get_serie(11, start="05-03-2016", end="25-10-2017"), correct)
        self.assertEqual(bcb.get_serie(11, start="05032016", end="25102017"), correct)

    ## Testing last_n argument

    def test_url_last_n(self):
        correct = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/30?formato=json"
        self.assertEqual(bcb.get_serie(11, last_n=30), correct)

    ## Testing crazy inputs

    def test_crazy_date(self):
        with self.assertRaises(ValueError):
            bcb.get_serie(11, start="asfhajksfsa")
            bcb.get_serie(11, start="002562345645")
            bcb.get_serie(11, start="###$%#RG")


@patch('seriesbr.bcb.return_search_results_bcb', mocked_search_results)
class TestBCBSearch(unittest.TestCase):

    def test_search(self):
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=spread&rows=10&start=1&sort=score desc"
        self.assertEqual(bcb.search("spread"), correct)

    def test_search_with_more_args(self):
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=spread&rows=10&start=1&sort=score desc&fq=mensal+livre"
        self.assertEqual(bcb.search("spread", "mensal", "livre"), correct)

    def test_search_with_more_args_and_rows(self):
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=spread&rows=30&start=5&sort=score desc&fq=mensal+livre"
        self.assertEqual(bcb.search("spread", "mensal", "livre", rows=30, skip=5), correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
