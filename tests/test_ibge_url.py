import os
import sys
import unittest
import datetime

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import ibge  # noqa: E402
from seriesbr.helpers.url import (  # noqa: E402
    ibge_make_classifications_query,
    ibge_make_variables_query,
)


def mocked_ibge_json_to_df(url, *args):
    return url


def mocked_today_date():
    return datetime.datetime(2019, 12, 2)


def mocked_list_regions(region, search, searches):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/{region}"
    return url


def mocked_get_frequency(code):
    return "mensal"


BASEURL = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos"


@patch("seriesbr.ibge.ibge_json_to_df", mocked_ibge_json_to_df)
@patch("seriesbr.helpers.dates.today_date", mocked_today_date)
@patch("seriesbr.ibge.get_frequency", mocked_get_frequency)
class IBGEtest(unittest.TestCase):

    maxDiff = None

    def test_url_no_dates(self):
        test = ibge.get_series(1419)
        expected = BASEURL + "/190001-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    # Testing year-only date formats

    def test_url_with_start_date_year_only(self):
        test = ibge.get_series(1419, start="2019")
        expected = BASEURL + "/201901-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    def test_url_end_date_year_only(self):
        test = ibge.get_series(1419, end="2018")
        expected = BASEURL + "/190001-201812/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    def test_url_start_and_end_date_year_only(self):
        test = ibge.get_series(1419, start="2017", end="2018")
        expected = BASEURL + "/201701-201812/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    # Testing month-year date formats

    def test_url_start_date_month_and_year(self):
        test = ibge.get_series(1419, start="09-2018")
        expected = BASEURL + "/201809-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    def test_url_end_date_month_and_year(self):
        test = ibge.get_series(1419, end="09/2018")
        expected = BASEURL + "/190001-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    def test_url_start_and_end_date_month_and_year(self):
        test = ibge.get_series(1419, start="07-2017", end="092018")
        expected = BASEURL + "/201707-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    # Testing complete dates -- shouldn't make any difference as days are ignore here

    def test_url_start_date_complete_dates(self):
        test = ibge.get_series(1419, start="03-09-2018")
        expected = BASEURL + "/201809-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    def test_url_end_date_complete_dates(self):
        test = ibge.get_series(1419, end="06/09/2018")
        expected = BASEURL + "/190001-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    def test_url_start_and_end_date_complete_dates(self):
        test = ibge.get_series(1419, start="05072017", end="12092018")
        expected = BASEURL + "/201707-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, expected)

    def test_ibge_make_classifications_query_simple(self):
        test = ibge_make_classifications_query(315)
        expected = "classificacao=315[all]"
        self.assertEqual(test, expected)

    def test_ibge_make_classifications_query_list(self):
        test = ibge_make_classifications_query([315, 22])
        expected = "classificacao=315[all]|22[all]"
        self.assertEqual(test, expected)

    def test_ibge_make_classifications_query_dict(self):
        test = ibge_make_classifications_query({315: [7169, 7170, 7445], 22: [1, 3]})
        expected = "classificacao=315[7169,7170,7445]|22[1,3]"
        self.assertEqual(test, expected)

    def test_ibge_make_variables_query_simple(self):
        test = ibge_make_variables_query(15)
        expected = "/variaveis/15"
        self.assertEqual(test, expected)

    def test_ibge_make_variables_query_list(self):
        test = ibge_make_variables_query([15, 16, 12])
        expected = "/variaveis/15|16|12"
        self.assertEqual(test, expected)

    def test_ibge_make_variables_query_none(self):
        test = ibge_make_variables_query(None)
        expected = "/variaveis"
        self.assertEqual(test, expected)

    def test_url_start_and_classifications(self):
        test = ibge.get_series(
            1419, start="07-2017", classifications={315: [7169, 7170]}
        )
        expected = (
            BASEURL
            + "/201707-201912/variaveis?classificacao=315[7169,7170]&localidades=BR&view=flat"  # noqa: W503
        )
        self.assertEqual(test, expected)

    @unittest.skipIf(sys.version_info.minor < 7, "Incompatible order of locations")
    def test_url_start_classifications_and_regions(self):
        expected = (
            BASEURL
            + "/201707-201912/variaveis/63?classificacao=315[7169,7170]&localidades=N7|BR&view=flat"  # noqa: W503
        )
        test = ibge.get_series(
            1419,
            variables=63,
            start="07-2017",
            mesoregions="all",
            brazil="yes",
            classifications={315: [7169, 7170]},
        )
        self.assertEqual(test, expected)

    def test_crazy_date(self):
        with self.assertRaises(ValueError):
            ibge.get_series(1419, start="asfhajksfsa")


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
