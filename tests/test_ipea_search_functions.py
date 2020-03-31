import os
import sys
import unittest
from unittest.mock import patch


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import ipea  # noqa: E402
from mock_helpers import get_sample_json, mock_json  # noqa: E402
from seriesbr.helpers.searching import ipea_get_search_results  # noqa: E402


def mocked_get_search_results_ipea(url):
    return url


@patch("seriesbr.ipea.ipea_get_search_results", mocked_get_search_results_ipea)
class TestIPEASearch(unittest.TestCase):

    base = "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados"

    def test_simple_search_filter(self):
        test = ipea.search(SERNOME="Spread")
        select_ = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"
        filter_ = "&$filter=contains(SERNOME,'Spread')"

        self.assertEqual(test, self.base + select_ + filter_)

    def test_simple_search_filter_no_name(self):
        test = ipea.search(UNINOME="%")
        select_ = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"
        filter_ = "&$filter=contains(UNINOME,'%')"

        self.assertEqual(test, self.base + select_ + filter_)

    def test_search_alpha_and_numeric_filter(self):
        test = ipea.search(SERNOME="Spread", TEMCODIGO=12)
        select_ = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,TEMCODIGO"
        filter_ = "&$filter=contains(SERNOME,'Spread') and TEMCODIGO eq 12"

        self.assertEqual(test, self.base + select_ + filter_)

    def test_search_three_filters_all_mixed(self):
        test = ipea.search(SERNOME="Spread", TEMCODIGO=12, FNTNOME="IBGE")
        select_ = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,TEMCODIGO,FNTNOME"
        filter_ = "&$filter=contains(SERNOME,'Spread') and TEMCODIGO eq 12 and contains(FNTNOME,'IBGE')"

        self.assertEqual(test, self.base + select_ + filter_)

    def test_search_without_name(self):
        test = ipea.search(TEMCODIGO=12, FNTNOME="IBGE")
        select_ = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,TEMCODIGO,FNTNOME"
        filter_ = "&$filter=TEMCODIGO eq 12 and contains(FNTNOME,'IBGE')"

        self.assertEqual(test, self.base + select_ + filter_)

    def test_search_without_name_equal_int(self):
        test = ipea.search(TEMCODIGO=12, FNTNOME="IBGE", SERNUMERICA=1)
        select_ = (
            "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,TEMCODIGO,FNTNOME,SERNUMERICA"
        )
        filter_ = (
            "&$filter=TEMCODIGO eq 12 and contains(FNTNOME,'IBGE') and SERNUMERICA eq 1"
        )

        self.assertEqual(test, self.base + select_ + filter_)

    def test_search_multiple_types_including_equal_string(self):
        test = ipea.search(
            SERNOME="Selic", TEMCODIGO=12, FNTNOME="IBGE", PAICODIGO="SAU"
        )
        select_ = (
            "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,TEMCODIGO,FNTNOME,PAICODIGO"
        )
        filter_ = "&$filter=contains(SERNOME,'Selic') and TEMCODIGO eq 12 and contains(FNTNOME,'IBGE') and PAICODIGO eq 'SAU'"

        self.assertEqual(test, self.base + select_ + filter_)

    def test_search_equal_operator_list_values_int(self):
        test = ipea.search(SERNOME="Selic", TEMCODIGO=[12, 14])
        select_ = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,TEMCODIGO"
        filter_ = "&$filter=contains(SERNOME,'Selic') and (TEMCODIGO eq 12 or TEMCODIGO eq 14)"

        self.assertEqual(test, self.base + select_ + filter_)

    def test_search_equal_operator_list_values_str(self):
        test = ipea.search(SERNOME="Selic", PAICODIGO=["USA", "BRA"])
        select_ = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,PAICODIGO"
        filter_ = "&$filter=contains(SERNOME,'Selic') and (PAICODIGO eq 'USA' or PAICODIGO eq 'BRA')"

        self.assertEqual(test, self.base + select_ + filter_)

    def test_search_all_list_values(self):
        test = ipea.search(
            SERNOME=["Selic", "Spread"], PAICODIGO=["USA", "BRA"], TEMCODIGO=[12, 13]
        )
        select_ = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,PAICODIGO,TEMCODIGO"
        filter_ = "&$filter=(contains(SERNOME,'Selic') or contains(SERNOME,'Spread')) and (PAICODIGO eq 'USA' or PAICODIGO eq 'BRA') and (TEMCODIGO eq 12 or TEMCODIGO eq 13)"

        self.assertEqual(test, self.base + select_ + filter_)

    def test_search_all_list_values_without_names(self):
        test = ipea.search(PAICODIGO=["USA", "BRA"], UNINOME=["%", "(% a.a.)"])
        select_ = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,PAICODIGO"
        filter_ = "&$filter=(PAICODIGO eq 'USA' or PAICODIGO eq 'BRA') and (contains(UNINOME,'%') or contains(UNINOME,'(% a.a.)'))"

        self.assertEqual(test, self.base + select_ + filter_)


class TestIpeaGetSearchResults(unittest.TestCase):
    def setUp(self):
        mock_json(
            path="seriesbr.helpers.searching.get_json",
            json=get_sample_json("ipea_search_results.json"),
        ).start()

    def test_ipea_get_search_results(self):
        df = ipea_get_search_results("url")

        self.assertFalse(df.empty)

    def tearDown(self):
        patch.stopall()


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
