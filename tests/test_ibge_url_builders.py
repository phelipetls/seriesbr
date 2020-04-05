import os
import sys
import unittest
import datetime

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import seriesbr.helpers.url as url  # noqa: E402


class TestUrlBuildersIBGE(unittest.TestCase):
    def test_make_classifications_query_str(self):
        test = url.ibge_make_classifications_query("315")
        expected = "classificacao=315[all]"
        self.assertEqual(test, expected)

    def test_make_classifications_query_int(self):
        test = url.ibge_make_classifications_query(315)
        expected = "classificacao=315[all]"
        self.assertEqual(test, expected)

    def test_make_classifications_query_dict(self):
        test = url.ibge_make_classifications_query({315: [11, 12, 13], 45: [7, 2]})
        expected = "classificacao=315[11,12,13]|45[7,2]"
        self.assertEqual(test, expected)

    def test_make_classifications_query_dict_empty_list(self):
        test = url.ibge_make_classifications_query({315: [], 45: [7, 2]})
        expected = "classificacao=315[all]|45[7,2]"
        self.assertEqual(test, expected)


def mocked_today_date():
    return datetime.datetime(2019, 12, 1)


class TestUrlBuildersDatesIBGE(unittest.TestCase):
    def test_make_dates_query_start_end(self):
        test = url.ibge_make_dates_query(start="02-2019", end="03-2019")
        expected = "/periodos/201902-201903"
        self.assertEqual(test, expected)

    @patch("seriesbr.helpers.dates.today_date", mocked_today_date)
    def test_make_dates_query_start(self):
        test = url.ibge_make_dates_query(start="02-2019", freq="mensal")
        expected = "/periodos/201902-201912"
        self.assertEqual(test, expected)

    def test_make_dates_query_end(self):
        test = url.ibge_make_dates_query(end="02-2019", freq="mensal")
        expected = "/periodos/190001-201902"
        self.assertEqual(test, expected)

    def test_make_dates_query_last_n(self):
        test = url.ibge_make_dates_query(last_n=4, freq="mensal")
        expected = "/periodos/-4"
        self.assertEqual(test, expected)

    def test_make_dates_query_yearly(self):
        test = url.ibge_make_dates_query(start="06-2018", end="02-2019", freq="anual")
        expected = "/periodos/2018-2019"
        self.assertEqual(test, expected)

    @patch("seriesbr.helpers.dates.today_date", mocked_today_date)
    def test_make_dates_query_monthly(self):
        test = url.ibge_make_dates_query()
        expected = "/periodos/190001-201912"
        self.assertEqual(test, expected)

    @patch("seriesbr.helpers.dates.today_date", mocked_today_date)
    def test_make_dates_query_quarterly(self):
        test = url.ibge_make_dates_query(freq="trimestral")
        expected = "/periodos/190001-201904"
        self.assertEqual(test, expected)

    def test_make_dates_query_quarterly_specific_dates(self):
        test = url.ibge_make_dates_query(start="2018", end="2018", freq="trimestral")
        expected = "/periodos/201801-201804"
        self.assertEqual(test, expected)


@unittest.skipIf(sys.version_info.minor < 7, "Incompatible order of locations")
class TestUrlBuildersLocationsIBGE(unittest.TestCase):
    def test_location_default_to_brazil(self):
        test = url.ibge_make_locations_query()
        expected = "&localidades=BR"
        self.assertEqual(test, expected)

    def test_location_brazil_kwarg_only(self):
        test = url.ibge_make_locations_query(brazil="yes")
        expected = "&localidades=BR"
        self.assertEqual(test, expected)

    def test_location_all_value(self):
        test = url.ibge_make_locations_query(municipality="all")
        expected = "&localidades=N6"
        self.assertEqual(test, expected)

    def test_location_boolean_value(self):
        test = url.ibge_make_locations_query(municipality=True)
        expected = "&localidades=N6"
        self.assertEqual(test, expected)

    def test_location_list_multiple_values(self):
        test = url.ibge_make_locations_query(municipality=[1, 2, 3])
        expected = "&localidades=N6[1,2,3]"
        self.assertEqual(test, expected)

    def test_location_list_single_value(self):
        test = url.ibge_make_locations_query(municipality=1)
        expected = "&localidades=N6[1]"
        self.assertEqual(test, expected)

    def test_location_multiple_municipalities(self):
        test = url.ibge_make_locations_query(municipality=["1", "2", "3"])
        expected = "&localidades=N6[1,2,3]"
        self.assertEqual(test, expected)

    def test_location_various_regions_boolean_values(self):
        test = url.ibge_make_locations_query(
            municipality=True, state=True, mesoregion=True
        )
        expected = "&localidades=N6|N3|N7"
        self.assertEqual(test, expected)

    def test_location_various_regions_mixed_values(self):
        test = url.ibge_make_locations_query(
            municipality=True, state=[4, 5], mesoregion="yes"
        )
        expected = "&localidades=N6|N3[4,5]|N7"
        self.assertEqual(test, expected)

    def test_mixed_kwargs_and_values(self):
        test = url.ibge_make_locations_query(
            municipality="all", state=[4, 5], brazil="yes"
        )
        expected = "&localidades=N6|N3[4,5]|BR"
        self.assertEqual(test, expected)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
