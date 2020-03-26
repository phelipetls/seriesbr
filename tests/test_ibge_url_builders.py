import os
import sys
import unittest
import datetime
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import seriesbr.helpers.url as url  # noqa: E402


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

    @patch("seriesbr.helpers.dates.today_date", mocked_today_date)
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

    @patch("seriesbr.helpers.dates.today_date", mocked_today_date)
    def test_make_dates_query_monthly(self):
        correct = "/periodos/190001-201912"
        test = url.ibge_make_dates_query()
        self.assertEqual(test, correct)

    @patch("seriesbr.helpers.dates.today_date", mocked_today_date)
    def test_make_dates_query_quarterly(self):
        correct = "/periodos/190001-201904"
        test = url.ibge_make_dates_query(freq="trimestral")
        self.assertEqual(test, correct)

    def test_make_dates_query_quarterly_specific_dates(self):
        correct = "/periodos/201801-201804"
        test = url.ibge_make_dates_query(start="2018", end="2018", freq="trimestral")
        self.assertEqual(test, correct)


@unittest.skipIf(sys.version_info.minor < 7, "Incompatible order of locations")
class TestUrlBuildersLocationsIBGE(unittest.TestCase):
    def test_location_default_to_brazil(self):
        correct = "&localidades=BR"
        test = url.ibge_make_locations_query()
        self.assertEqual(test, correct)

    def test_location_brazil_kwarg_only(self):
        correct = "&localidades=BR"
        test = url.ibge_make_locations_query(brazil="yes")
        self.assertEqual(test, correct)

    def test_location_all_value(self):
        correct = "&localidades=N6"
        test = url.ibge_make_locations_query(municipality="all")
        self.assertEqual(test, correct)

    def test_location_boolean_value(self):
        correct = "&localidades=N6"
        test = url.ibge_make_locations_query(municipality=True)
        self.assertEqual(test, correct)

    def test_location_list_multiple_values(self):
        correct = "&localidades=N6[1,2,3]"
        test = url.ibge_make_locations_query(municipality=[1, 2, 3])
        self.assertEqual(test, correct)

    def test_location_list_single_value(self):
        correct = "&localidades=N6[1]"
        test = url.ibge_make_locations_query(municipality=1)
        self.assertEqual(test, correct)

    def test_location_multiple_municipalities(self):
        correct = "&localidades=N6[1,2,3]"
        test = url.ibge_make_locations_query(municipality=["1", "2", "3"])
        self.assertEqual(test, correct)

    def test_location_various_regions_boolean_values(self):
        correct = "&localidades=N6|N3|N7"
        test = url.ibge_make_locations_query(
            municipality=True, state=True, mesoregion=True
        )
        self.assertEqual(test, correct)

    def test_location_various_regions_mixed_values(self):
        correct = "&localidades=N6|N3[4,5]|N7"
        test = url.ibge_make_locations_query(
            municipality=True, state=[4, 5], mesoregion="yes"
        )
        self.assertEqual(test, correct)

    def test_mixed_kwargs_and_values(self):
        correct = "&localidades=N6|N3[4,5]|BR"
        test = url.ibge_make_locations_query(
            municipality="all", state=[4, 5], brazil="yes"
        )
        self.assertEqual(test, correct)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
