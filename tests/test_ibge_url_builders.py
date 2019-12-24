import os
import sys
import unittest
import datetime
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import seriesbr.helpers.url as url


class TestUrlBuildersIBGE(unittest.TestCase):

    def test_make_classifications_query_str(self):
        correct = "classificacao=315[all]"
        test = url.ibge_make_classifications_query("315")
        self.assertEqual(test, correct)

    def test_make_classifications_query_int(self):
        correct = "classificacao=315[all]"
        test = url.ibge_make_classifications_query(315)
        self.assertEqual(test, correct)

    def test_make_classifications_query_dict(self):
        correct = "classificacao=315[11,12,13]|45[7,2]"
        test = url.ibge_make_classifications_query({315: [11, 12, 13], 45: [7, 2]})
        self.assertEqual(test, correct)

    def test_make_classifications_query_dict_empty_list(self):
        correct = "classificacao=315[all]|45[7,2]"
        test = url.ibge_make_classifications_query({315: [], 45: [7, 2]})
        self.assertEqual(test, correct)


def mocked_today_date():
    return datetime.datetime(2019, 12, 1)


class TestUrlBuildersDatesIBGE(unittest.TestCase):

    def test_make_dates_query_start_end(self):
        correct = "/periodos/201902-201903"
        test = url.ibge_make_dates_query(start="02-2019", end="03-2019")
        self.assertEqual(test, correct)

    @patch('seriesbr.helpers.url.today_date', mocked_today_date)
    def test_make_dates_query_start(self):
        correct = "/periodos/201902-201912"
        test = url.ibge_make_dates_query(start="02-2019", freq="mensal")
        self.assertEqual(test, correct)

    def test_make_dates_query_end(self):
        correct = "/periodos/190001-201902"
        test = url.ibge_make_dates_query(end="02-2019", freq="mensal")
        self.assertEqual(test, correct)

    def test_make_dates_query_last_n(self):
        correct = "/periodos/-4"
        test = url.ibge_make_dates_query(last_n=4, freq="mensal")
        self.assertEqual(test, correct)

    def test_make_dates_query_yearly(self):
        correct = "/periodos/2018-2019"
        test = url.ibge_make_dates_query(start="06-2018", end="02-2019", freq="anual")
        self.assertEqual(test, correct)

    @patch('seriesbr.helpers.url.today_date', mocked_today_date)
    def test_make_dates_query_monthly(self):
        correct = "/periodos/190001-201912"
        test = url.ibge_make_dates_query()
        self.assertEqual(test, correct)

    @patch('seriesbr.helpers.url.today_date', mocked_today_date)
    def test_make_dates_query_quarterly(self):
        correct = "/periodos/190001-201904"
        test = url.ibge_make_dates_query(freq="trimestral")
        self.assertEqual(test, correct)

    def test_make_dates_raise_if_not_quarter(self):
        with self.assertRaises(ValueError):
            url.ibge_make_dates_query(end="12-2018", freq="trimestral")


class TestUrlBuildersLocationsIBGE(unittest.TestCase):

    @unittest.skipIf(sys.version_info.minor < 7, "Incompatible order of locations")
    def test_make_cities_query(self):
        correct = [
            "&localidades=N6[1]",
            "&localidades=N6[1,2,3]",
            "&localidades=N6[all]",
            "&localidades=N6[all]|N3[4,5]|BR",
            "&localidades=N6[all]|N3[4,5]",
            "&localidades=N6[all]|N3[4,5]|N7[all]",
            "&localidades=N6[all]|N3[all]|N7[all]",
            "&localidades=N6[1,2,3]",
            "&localidades=N6[all]",
            "&localidades=BR",
            "&localidades=BR"
        ]
        test = [
            url.ibge_make_locations_query(city=1),
            url.ibge_make_locations_query(city=[1, 2, 3]),
            url.ibge_make_locations_query(city="all"),
            url.ibge_make_locations_query(city="all", state=[4, 5], brazil="yes"),
            url.ibge_make_locations_query(city=True, state=[4, 5]),
            url.ibge_make_locations_query(city=True, state=[4, 5], mesoregion="yes"),
            url.ibge_make_locations_query(city=True, state=True, mesoregion=True),
            url.ibge_make_locations_query(city=["1", "2", "3"]),
            url.ibge_make_locations_query(city=["all"]),
            url.ibge_make_locations_query(brazil="yes"),
            url.ibge_make_locations_query()
        ]
        self.assertListEqual(test, correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
