import os
import sys
import unittest
import datetime

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import ipea  # noqa: E402


def mocked_json_to_df(url, code, name):
    return url


def mocked_today_date():
    return datetime.datetime(2019, 12, 2)


URL = "http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='BM12_CRLIN12')?$select=VALDATA,VALVALOR"


@patch("seriesbr.ipea.ipea_json_to_df", mocked_json_to_df)
@patch("seriesbr.helpers.dates.today_date", mocked_today_date)
class IPEAtest(unittest.TestCase):

    maxDiff = None

    def test_url_no_dates(self):
        test = ipea.get_serie("BM12_CRLIN12")
        correct = (
            URL
            + "&$filter=VALDATA ge 1900-01-01T00:00:00-00:00 and VALDATA le 2019-12-02T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)

    # Test only with start dates

    def test_url_start_dates_complete_dates(self):
        test = ipea.get_serie("BM12_CRLIN12", start="01-02-2019")
        correct = (
            URL
            + "&$filter=VALDATA ge 2019-02-01T00:00:00-00:00 and VALDATA le 2019-12-02T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)

    def test_url_start_dates_month_year(self):
        test = ipea.get_serie("BM12_CRLIN12", start="02/2019")
        correct = (
            URL
            + "&$filter=VALDATA ge 2019-02-01T00:00:00-00:00 and VALDATA le 2019-12-02T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)

    def test_url_start_dates_year_only(self):
        test = ipea.get_serie("BM12_CRLIN12", start="2019")
        correct = (
            URL
            + "&$filter=VALDATA ge 2019-01-01T00:00:00-00:00 and VALDATA le 2019-12-02T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)

    # Test only with end dates

    def test_url_end_dates_complete_dates(self):
        test = ipea.get_serie("BM12_CRLIN12", end="01022019")
        correct = (
            URL
            + "&$filter=VALDATA ge 1900-01-01T00:00:00-00:00 and VALDATA le 2019-02-01T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)

    def test_url_end_dates_month_year(self):
        test = ipea.get_serie("BM12_CRLIN12", end="02-2019")
        correct = (
            URL
            + "&$filter=VALDATA ge 1900-01-01T00:00:00-00:00 and VALDATA le 2019-02-28T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)

    def test_url_end_dates_year_only(self):
        test = ipea.get_serie("BM12_CRLIN12", end="2019")
        correct = (
            URL
            + "&$filter=VALDATA ge 1900-01-01T00:00:00-00:00 and VALDATA le 2019-12-31T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)

    # Test with both start and end dates

    def test_url_start_and_end_dates_complete_dates(self):
        test = ipea.get_serie("BM12_CRLIN12", start="04-05-2016", end="01-02-2019")
        correct = (
            URL
            + "&$filter=VALDATA ge 2016-05-04T00:00:00-00:00 and VALDATA le 2019-02-01T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)

    def test_url_start_and_end_dates_month_year(self):
        test = ipea.get_serie("BM12_CRLIN12", start="052016", end="022019")
        correct = (
            URL
            + "&$filter=VALDATA ge 2016-05-01T00:00:00-00:00 and VALDATA le 2019-02-28T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)

    def test_url_start_and_end_dates_year_only(self):
        test = ipea.get_serie("BM12_CRLIN12", start="2016", end="2019")
        correct = (
            URL
            + "&$filter=VALDATA ge 2016-01-01T00:00:00-00:00 and VALDATA le 2019-12-31T00:00:00-00:00"  # noqa: W503
        )
        self.assertEqual(test, correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
