import os
import sys
import unittest
import datetime

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ibge
from seriesbr.helpers.url import (
    ibge_make_classifications_query,
    ibge_make_variables_query,
)


def mocked_ibge_json_to_df(url, frequency):
    return url


def mocked_today_date():
    return datetime.datetime(2019, 12, 2)


def mocked_list_regions(region, search, searches):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/{region}"
    return url


def mocked_get_frequency(code):
    return "mensal"


@patch('seriesbr.ibge.ibge_json_to_df', mocked_ibge_json_to_df)
@patch('seriesbr.helpers.dates.today_date', mocked_today_date)
@patch('seriesbr.ibge.get_frequency', mocked_get_frequency)
class IBGEtest(unittest.TestCase):

    maxDiff = None

    def test_url_no_dates(self):
        test = ibge.get_series(1419)
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/190001-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    ## Testing year-only date formats

    def test_url_with_start_date_year_only(self):
        test = ibge.get_series(1419, start="2019")
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201901-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    def test_url_end_date_year_only(self):
        test = ibge.get_series(1419, end="2018")
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/190001-201812/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    def test_url_start_and_end_date_year_only(self):
        test = ibge.get_series(1419, start="2017", end="2018")
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201701-201812/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    ## Testing month-year date formats

    def test_url_start_date_month_and_year(self):
        test = ibge.get_series(1419, start="09-2018")
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201809-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    def test_url_end_date_month_and_year(self):
        test = ibge.get_series(1419, end="09/2018")
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/190001-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    def test_url_start_and_end_date_month_and_year(self):
        test = ibge.get_series(1419, start="07-2017", end="092018")
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201707-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    ## Testing complete dates -- shouldn't make any difference as days are ignore here

    def test_url_start_date_complete_dates(self):
        test = ibge.get_series(1419, start="03-09-2018")
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201809-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    def test_url_end_date_complete_dates(self):
        test = ibge.get_series(1419, end="06/09/2018")
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/190001-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    def test_url_start_and_end_date_complete_dates(self):
        test = ibge.get_series(1419, start="05072017", end="12092018")
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201707-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    def test_ibge_make_classifications_query_simple(self):
        test = ibge_make_classifications_query(315)
        correct = "classificacao=315[all]"
        self.assertEqual(test, correct)

    def test_ibge_make_classifications_query_list(self):
        test = ibge_make_classifications_query([315, 22])
        correct = "classificacao=315[all]|22[all]"
        self.assertEqual(test, correct)

    def test_ibge_make_classifications_query_dict(self):
        test = ibge_make_classifications_query({315: [7169, 7170, 7445], 22: [1, 3]})
        correct = "classificacao=315[7169,7170,7445]|22[1,3]"
        self.assertEqual(test, correct)

    def test_ibge_make_variables_query_simple(self):
        test = ibge_make_variables_query(15)
        correct = "/variaveis/15"
        self.assertEqual(test, correct)

    def test_ibge_make_variables_query_list(self):
        test = ibge_make_variables_query([15, 16, 12])
        correct = "/variaveis/15|16|12"
        self.assertEqual(test, correct)

    def test_ibge_make_variables_query_none(self):
        test = ibge_make_variables_query(None)
        correct = "/variaveis"
        self.assertEqual(test, correct)

    def test_url_start_and_classifications(self):
        test = ibge.get_series(1419, start="07-2017", classifications={315: [7169, 7170]})
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201707-201912/variaveis?classificacao=315[7169,7170]&localidades=BR&view=flat"
        self.assertEqual(test, correct)

    @unittest.skipIf(sys.version_info.minor < 7, "Incompatible order of locations")
    def test_url_start_classifications_and_regions(self):
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201707-201912/variaveis/63?classificacao=315[7169,7170]&localidades=N7[all]|BR&view=flat"
        test = ibge.get_series(1419, variables=63, start="07-2017", mesoregion="all", brazil="yes", classifications={315: [7169, 7170]})
        self.assertEqual(test, correct)

    def test_crazy_date(self):
        with self.assertRaises(ValueError):
            ibge.get_series(1419, start="asfhajksfsa")


@patch('seriesbr.ibge.list_regions_helper', mocked_list_regions)
class TestListsFunctions(unittest.TestCase):

    def test_list_cities(self):
        test = ibge.list_cities()
        correct = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        self.assertEqual(test, correct)

    def test_list_regions(self):
        test = ibge.list_macroregions()
        correct = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes"
        self.assertEqual(test, correct)

    def test_list_mesoregions(self):
        test = ibge.list_mesoregions()
        correct = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
        self.assertEqual(test, correct)

    def test_list_microregions(self):
        test = ibge.list_microregions()
        correct = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
        self.assertEqual(test, correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
