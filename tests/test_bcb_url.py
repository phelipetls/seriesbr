import unittest

from seriesbr import bcb
from unittest.mock import patch
from mock_helpers import mocked_get_today_date


URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?format=json"


@patch("seriesbr.helpers.dates.get_today_date", mocked_get_today_date)
class TestBcbUrl(unittest.TestCase):
    """Test Bcb url builder to get a time series"""

    def test_no_dates(self):
        url = bcb.build_url(11)
        expected_url = "&dataInicial=01/01/1900&dataFinal=02/12/2019"

        self.assertEqual(url, f"{URL}{expected_url}")

    def test_start_date_year_only(self):
        url = bcb.build_url(11, start="2013")
        expected_url = "&dataInicial=01/01/2013&dataFinal=02/12/2019"

        self.assertEqual(url, f"{URL}{expected_url}")

    def test_start_date_month_and_year(self):
        url = bcb.build_url(11, start="07-2013")
        expected_url = "&dataInicial=01/07/2013&dataFinal=02/12/2019"

        self.assertEqual(url, f"{URL}{expected_url}")

    def test_end_date_year_only(self):
        url = bcb.build_url(11, end="1990")
        expected_url = "&dataInicial=01/01/1900&dataFinal=31/12/1990"

        self.assertEqual(url, f"{URL}{expected_url}")

    def test_end_date_month_and_year(self):
        url = bcb.build_url(11, end="06-1990")
        expected_url = "&dataInicial=01/01/1900&dataFinal=30/06/1990"

        self.assertEqual(url, f"{URL}{expected_url}")

    def test_end_date_full(self):
        url = bcb.build_url(11, end="05-03-2016")
        expected_url = "&dataInicial=01/01/1900&dataFinal=05/03/2016"

        self.assertEqual(url, f"{URL}{expected_url}")

    def test_start_and_end_date_year_only(self):
        url = bcb.build_url(11, start="2013", end="09/2014")
        expected_url = "&dataInicial=01/01/2013&dataFinal=30/09/2014"

        self.assertEqual(url, f"{URL}{expected_url}")

    def test_start_and_end_date_month_and_year(self):
        url = bcb.build_url(11, start="07-2013", end="09-2014")
        expected_url = "&dataInicial=01/07/2013&dataFinal=30/09/2014"

        self.assertEqual(url, f"{URL}{expected_url}")

    def test_start_and_end_date_full_dates(self):
        url = bcb.build_url(11, start="05-03-2016", end="25-10-2017")
        expected_url = "&dataInicial=05/03/2016&dataFinal=25/10/2017"

        self.assertEqual(url, f"{URL}{expected_url}")

    def test_last_n(self):
        url = bcb.build_url(11, last_n=30)
        expected_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/30?format=json"

        self.assertEqual(url, expected_url)

    def test_invalid_code(self):
        with self.assertRaises(AssertionError):
            bcb.build_url({})

    def test_crazy_date(self):
        with self.assertRaises(ValueError):
            bcb.build_url(11, start="asfhajksfsa")


if __name__ == "__main__":
    unittest.main(failfast=True)
