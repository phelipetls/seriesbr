import os
import sys
import unittest
import datetime

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import bcb  # noqa: E402


def mocked_json_to_df(url, *args):
    """Instead of parsing the JSON, just return the URL"""
    return url


def mocked_today_date():
    """Use this date as if it were today"""
    return datetime.datetime(2019, 12, 2)


BASEURL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?format=json"


@patch("seriesbr.bcb.bcb_json_to_df", mocked_json_to_df)
@patch("seriesbr.helpers.dates.today_date", mocked_today_date)
class BCBtest(unittest.TestCase):
    def test_url_no_dates(self):
        expected = BASEURL + "&dataInicial=01/01/1900&dataFinal=02/12/2019"
        self.assertEqual(bcb.get_serie(11), expected)

    # Testing start dates argument

    def test_url_start_date_year_only(self):
        expected = BASEURL + "&dataInicial=01/01/2013&dataFinal=02/12/2019"
        self.assertEqual(bcb.get_serie(11, start="2013"), expected)

    def test_url_start_date_month_and_year(self):
        expected = BASEURL + "&dataInicial=01/07/2013&dataFinal=02/12/2019"
        self.assertEqual(bcb.get_serie(11, start="07-2013"), expected)

    # Testing end dates argument

    def test_url_end_date_year_only(self):
        expected = BASEURL + "&dataInicial=01/01/1900&dataFinal=31/12/1990"
        self.assertEqual(bcb.get_serie(11, end="1990"), expected)

    def test_url_end_date_month_and_year(self):
        expected = BASEURL + "&dataInicial=01/01/1900&dataFinal=30/06/1990"
        self.assertEqual(bcb.get_serie(11, end="06-1990"), expected)

    def test_url_complete_dates(self):
        expected = BASEURL + "&dataInicial=01/01/1900&dataFinal=05/03/2016"
        self.assertEqual(bcb.get_serie(11, end="05032016"), expected)

    # Testing start and end dates arguments

    def test_url_start_and_end_date_year_only(self):
        expected = BASEURL + "&dataInicial=01/01/2013&dataFinal=30/09/2014"
        self.assertEqual(bcb.get_serie(11, start="2013", end="09/2014"), expected)

    def test_url_start_and_end_date_month_and_year(self):
        expected = BASEURL + "&dataInicial=01/07/2013&dataFinal=30/09/2014"
        self.assertEqual(bcb.get_serie(11, start="07-2013", end="09-2014"), expected)

    def test_url_start_and_end_date_complete_dates(self):
        expected = BASEURL + "&dataInicial=05/03/2016&dataFinal=25/10/2017"
        self.assertEqual(bcb.get_serie(11, start="05032016", end="25102017"), expected)

    # Testing last_n argument

    def test_url_last_n(self):
        expected = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/30?formato=json"
        self.assertEqual(bcb.get_serie(11, last_n=30), expected)

    # Testing invalid inputs

    def test_crazy_date(self):
        with self.assertRaises(ValueError):
            bcb.get_serie(11, start="asfhajksfsa")
            bcb.get_serie(11, start="002562345645")
            bcb.get_serie(11, start="###$%#RG")


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
