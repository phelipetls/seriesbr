import os
import sys
import unittest
import datetime

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ibge
from seriesbr.helpers.url import (
    ibge_make_classification_query,
    ibge_make_variables_query,
)


def mocked_get_json(url):
    return url


def mocked_ibge_json_to_df(json, frequency):
    return json


def mocked_today_date():
    return datetime.datetime(2019, 12, 2)


def mocked_list_regions(kind_of_region, search=None, where="nome"):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/{kind_of_region}"
    return url


@patch('seriesbr.ibge.get_json', mocked_get_json)
@patch('seriesbr.ibge.ibge_json_to_df', mocked_ibge_json_to_df)
@patch('seriesbr.helpers.dates.today_date', mocked_today_date)
class IBGEtest(unittest.TestCase):

    maxDiff = None

    @patch('seriesbr.ibge.get_frequency')
    def test_url_no_dates(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/190001-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419), correct)

    ## Testing year-only date formats

    @patch('seriesbr.ibge.get_frequency')
    def test_url_with_start_date_year_only(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201901-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419, start="2019"), correct)

    @patch('seriesbr.ibge.get_frequency')
    def test_url_end_date_year_only(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/190001-201812/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419, end="2018"), correct)

    @patch('seriesbr.ibge.get_frequency')
    def test_url_start_and_end_date_year_only(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201701-201812/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419, start="2017", end="2018"), correct)

    ## Testing month-year date formats

    @patch('seriesbr.ibge.get_frequency')
    def test_url_start_date_month_and_year(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201809-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419, start="09-2018"), correct)
        self.assertEqual(ibge.get_series(1419, start="09/2018"), correct)
        self.assertEqual(ibge.get_series(1419, start="092018"), correct)

    @patch('seriesbr.ibge.get_frequency')
    def test_url_end_date_month_and_year(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/190001-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419, end="09-2018"), correct)
        self.assertEqual(ibge.get_series(1419, end="09/2018"), correct)
        self.assertEqual(ibge.get_series(1419, end="092018"), correct)

    @patch('seriesbr.ibge.get_frequency')
    def test_url_start_and_end_date_month_and_year(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201707-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419, start="07-2017", end="09-2018"), correct)
        self.assertEqual(ibge.get_series(1419, start="07-2017", end="09/2018"), correct)
        self.assertEqual(ibge.get_series(1419, start="07-2017", end="092018"), correct)

    ## Testing complete dates -- shouldn't make any difference as days are ignore here

    @patch('seriesbr.ibge.get_frequency')
    def test_url_start_date_complete_dates(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201809-201912/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419, start="03-09-2018"), correct)
        self.assertEqual(ibge.get_series(1419, start="03/09/2018"), correct)
        self.assertEqual(ibge.get_series(1419, start="03092018"), correct)

    @patch('seriesbr.ibge.get_frequency')
    def test_url_end_date_complete_dates(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/190001-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419, end="06-09-2018"), correct)
        self.assertEqual(ibge.get_series(1419, end="06/09/2018"), correct)
        self.assertEqual(ibge.get_series(1419, end="06092018"), correct)

    @patch('seriesbr.ibge.get_frequency')
    def test_url_start_and_end_date_complete_dates(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201707-201809/variaveis?&localidades=BR&view=flat"
        self.assertEqual(ibge.get_series(1419, start="05-07-2017", end="12-09-2018"), correct)
        self.assertEqual(ibge.get_series(1419, start="05/07/2017", end="12/09/2018"), correct)
        self.assertEqual(ibge.get_series(1419, start="05072017", end="12092018"), correct)

    @patch('seriesbr.ibge.get_frequency')
    def test_ibge_make_classification_query(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        self.assertEqual(ibge_make_classification_query({315: [7169, 7170, 7445], 22: [1, 3]}), "classificacao=315[7169,7170,7445]|22[1,3]")
        self.assertEqual(ibge_make_classification_query(315), "classificacao=315[all]")
        self.assertEqual(ibge_make_classification_query([315, 22]), "classificacao=315[all]|22[all]")

    @patch('seriesbr.ibge.get_frequency')
    def test_ibge_make_variables_query(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        self.assertEqual(ibge_make_variables_query(15), "/variaveis/15")
        self.assertEqual(ibge_make_variables_query([15, 16, 12]), "/variaveis/15|16|12")
        self.assertEqual(ibge_make_variables_query(None), "/variaveis")

    @patch('seriesbr.ibge.get_frequency')
    def test_url_start_and_classifications(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201707-201912/variaveis?classificacao=315[7169,7170]&localidades=BR&view=flat"
        test = ibge.get_series(1419, start="07-2017", classifications={315: [7169, 7170]})
        self.assertEqual(test, correct)

    @patch('seriesbr.ibge.get_frequency')
    @unittest.skipIf(sys.version_info.minor < 7, "Incompatible order of locations")
    def test_url_start_classifications_and_regions(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        correct = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201707-201912/variaveis/63?classificacao=315[7169,7170]&localidades=N7[all]|BR&view=flat"
        test = ibge.get_series(1419, variables=63, start="07-2017", mesoregion="all", brazil="yes", classifications={315: [7169, 7170]})
        self.assertEqual(test, correct)

    @patch('seriesbr.ibge.get_frequency')
    def test_crazy_date(self, mocked_get_frequency):
        mocked_get_frequency.return_value = "mensal"
        with self.assertRaises(ValueError):
            ibge.get_series(1419, start="asfhajksfsa")
            ibge.get_series(1419, start="002562345645")
            ibge.get_series(1419, start="###$%#RG")


@patch('seriesbr.ibge.list_regions', mocked_list_regions)
class TestListsFunctions(unittest.TestCase):

    def test_list_cities(self):
        correct = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        self.assertEqual(ibge.list_cities(), correct)

    def test_list_regions(self):
        correct = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes"
        self.assertEqual(ibge.list_macroregions(), correct)

    def test_list_mesoregions(self):
        correct = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
        self.assertEqual(ibge.list_mesoregions(), correct)

    def test_list_microregions(self):
        correct = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
        self.assertEqual(ibge.list_microregions(), correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
